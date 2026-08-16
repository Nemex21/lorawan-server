"""
SQLAlchemy database models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum

Base = declarative_base()


class MessageType(str, Enum):
    """Message types"""
    EMERGENCY = "emergency"
    NORMAL = "normal"
    ALERT = "alert"
    HEARTBEAT = "heartbeat"


class MessageStatus(str, Enum):
    """Message status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    EXPIRED = "expired"


class Message(Base):
    """Message database model"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), index=True, nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(SQLEnum(MessageType), default=MessageType.NORMAL, nullable=False)
    status = Column(SQLEnum(MessageStatus), default=MessageStatus.PENDING, nullable=False)
    priority = Column(Integer, default=5, nullable=False)
    ttl = Column(Integer, default=3600, nullable=False)
    encrypted = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    delivered_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True, index=True)
    
    def __repr__(self):
        return f"<Message(id={self.id}, device_id={self.device_id}, status={self.status})>"
