from pydantic import BaseModel, Field, conint
from typing import Optional, Any, List
from datetime import datetime

# ---- Requests ----
class RecordCreate(BaseModel):
    project_name: str
    registry: str
    vintage: conint(ge=1900, le=2100)
    quantity: conint(gt=0)
    serial_number: Optional[str] = None

# ---- Responses ----
class RecordOut(BaseModel):
    id: str
    project_name: str
    registry: str
    vintage: int
    quantity: int
    serial_number: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}  

class EventOut(BaseModel):
    event_id: int
    record_id: str
    event_type: str
    created_at: datetime

    model_config = {"from_attributes": True}

class RecordWithEvents(BaseModel):
    record: RecordOut
    events: List[EventOut]
