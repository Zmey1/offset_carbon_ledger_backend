from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas, utils

def create_record(db: Session, payload: schemas.RecordCreate) -> models.CreditRecord:
    rec_id = utils.deterministic_id(
        payload.project_name, payload.registry, payload.vintage, payload.quantity
    )

    # if rec_id exists, return it instead of creating a duplicate.
    existing = db.get(models.CreditRecord, rec_id)
    if existing:
        return existing

    rec = models.CreditRecord(
        id=rec_id,
        project_name=payload.project_name,
        registry=payload.registry,
        vintage=payload.vintage,
        quantity=payload.quantity,
        serial_number=payload.serial_number
    )
    db.add(rec)
    db.flush()  # ensure record_id is usable before writing the event

    # Append 'created' event to start the ledger history
    db.add(models.Event(record_id=rec_id, event_type="created", details=None))

    db.commit()
    db.refresh(rec)
    return rec

def get_record_with_events(db: Session, rec_id: str):
    rec = db.get(models.CreditRecord, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")

    events = (
        db.query(models.Event)
          .filter(models.Event.record_id == rec_id)
          .order_by(models.Event.event_id.asc())
          .all()
    )
    return rec, events

def retire_record(db: Session, rec_id: str) -> None:
    rec = db.get(models.CreditRecord, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")

    try:
        db.add(models.Event(record_id=rec_id, event_type="retired", details=None))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Already retired")
    
def sell_record(db: Session, rec_id: str) -> None:
    rec = db.get(models.CreditRecord, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")

    # if already sold
    already_sold = (
        db.query(models.Event)
          .filter(models.Event.record_id == rec_id, models.Event.event_type == "sold")
          .first()
    )
    if already_sold:
        raise HTTPException(status_code=409, detail="Already sold")

    #if already retired
    already_retired = (
        db.query(models.Event)
          .filter(models.Event.record_id == rec_id, models.Event.event_type == "retired")
          .first()
    )
    if already_retired:
        raise HTTPException(status_code=400, detail="Cannot sell a retired credit")

    # Create sold event
    db.add(models.Event(record_id=rec_id, event_type="sold", details=None))
    db.commit()
