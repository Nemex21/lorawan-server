"""
Message model
"""

from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, func
from datetime import datetime
from pydantic import BaseModel
from app.models.base import Base
from typing import Optional


class Message(Base):
    """
    LoRaWAN message model
    """
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    is_encrypted = Column(Boolean, default=False)
    rssi = Column(Integer, nullable=True)  # Signal strength
    snr = Column(Float, nullable=True)  # Signal-to-noise ratio
    frequency = Column(Float, nullable=True)  # Frequency in MHz
    data_rate = Column(String, nullable=True)  # Data rate (e.g., SF7BW125)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class MessageSchema(BaseModel):
    """
    Message response schema
    """
    id: str
    device_id: str
    content: str
    is_encrypted: bool
    rssi: Optional[int] = None
    snr: Optional[float] = None
    frequency: Optional[float] = None
    data_rate: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True


class MessageCreateSchema(BaseModel):
    """
    Message create request schema
    """
    device_id: str
    content: str
    is_encrypted: bool = False
    rssi: Optional[int] = None
    snr: Optional[float] = None
    frequency: Optional[float] = None
    data_rate: Optional[str] = None
