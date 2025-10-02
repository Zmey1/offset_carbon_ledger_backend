from sqlalchemy import Column, String, Integer, Text, JSON, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class CreditRecord(Base):
    __tablename__ = "records"

    id = Column(String(64), primary_key=True, index=True)
    project_name = Column(Text, nullable=False)
    registry = Column(Text, nullable=False)
    vintage = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    serial_number = Column(Text)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(String(64), nullable=False, index=True)
    event_type = Column(Text, nullable=False)   # 'created', 'retired'
    details = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())
