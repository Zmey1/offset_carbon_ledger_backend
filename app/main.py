from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import schemas, crud

app = FastAPI(title="Carbon Credit Ledger")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/records", response_model=schemas.RecordOut, status_code=201)
def create_record(body: schemas.RecordCreate, db: Session = Depends(get_db)):
    rec = crud.create_record(db, body)
    return schemas.RecordOut.model_validate(rec, from_attributes=True)

@app.get("/records/{rec_id}", response_model=schemas.RecordWithEvents)
def get_record(rec_id: str, db: Session = Depends(get_db)):
    rec, events = crud.get_record_with_events(db, rec_id)
    return {
        "record": schemas.RecordOut.model_validate(rec, from_attributes=True),
        "events": [schemas.EventOut.model_validate(e, from_attributes=True) for e in events],
    }

@app.post("/records/{rec_id}/retire")
def retire_record(rec_id: str, db: Session = Depends(get_db)):
    crud.retire_record(db, rec_id)
    return {"status": "retired"}

@app.post("/records/{rec_id}/sell")
def sell_record(rec_id: str, db: Session = Depends(get_db)):
    crud.sell_record(db, rec_id)
    return {"status": "sold"}

