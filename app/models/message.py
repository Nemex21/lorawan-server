"""
Message model for LoRaWAN messages
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class Message(Base):
    """SQLAlchemy Message model"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    device_id = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    is_encrypted = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    received_at = Column(DateTime, default=datetime.utcnow)
    rssi = Column(Integer, nullable=True)
    snr = Column(Integer, nullable=True)
    frequency = Column(Integer, nullable=True)
    data_rate = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Message(id={self.id}, device_id={self.device_id}, timestamp={self.timestamp})>"


class MessageSchema(BaseModel):
    """Pydantic schema for Message"""
    id: str
    device_id: str
    content: str
    is_encrypted: bool = False
    timestamp: datetime
    received_at: datetime
    rssi: Optional[int] = None
    snr: Optional[int] = None
    frequency: Optional[int] = None
    data_rate: Optional[str] = None
    
    class Config:
        from_attributes = True


class MessageCreateSchema(BaseModel):
    """Schema for creating a message"""
    device_id: str
    content: str
    is_encrypted: bool = False
    rssi: Optional[int] = None
    snr: Optional[int] = None
    frequency: Optional[int] = None
    data_rate: Optional[str] = None
