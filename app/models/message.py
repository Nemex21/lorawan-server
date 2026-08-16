"""
Message data models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


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


class MessageCreate(BaseModel):
    """Request model for creating a message"""
    device_id: str = Field(..., description="Device ID")
    content: str = Field(..., min_length=1, max_length=255, description="Message content")
    message_type: MessageType = Field(default=MessageType.NORMAL)
    priority: int = Field(default=5, ge=1, le=10, description="Priority level 1-10")
    ttl: Optional[int] = Field(default=None, description="Time to live in seconds")


class MessageUpdate(BaseModel):
    """Request model for updating a message"""
    status: MessageStatus
    delivered_at: Optional[datetime] = None


class MessageResponse(BaseModel):
    """Response model for a message"""
    id: int
    device_id: str
    content: str
    message_type: MessageType
    status: MessageStatus
    priority: int
    ttl: int
    encrypted: bool
    created_at: datetime
    delivered_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MessageBatch(BaseModel):
    """Response model for message batch"""
    total: int
    pending: int
    delivered: int
    failed: int
    expired: int
    messages: list[MessageResponse]
