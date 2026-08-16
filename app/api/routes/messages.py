"""
Message API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import MessageCreate, MessageUpdate, MessageResponse, MessageBatch, MessageStatus
from app.database.models import Message
from app.database.connection import get_db
from app.services import encryption_service
from datetime import datetime, timedelta

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Create a new message"""
    # Calculate expiration time
    expires_at = datetime.utcnow() + timedelta(seconds=message.ttl) if message.ttl else None
    
    # Encrypt content
    encrypted_content = encryption_service.encrypt(message.content)
    
    db_message = Message(
        device_id=message.device_id,
        content=encrypted_content,
        message_type=message.message_type,
        status=MessageStatus.PENDING,
        priority=message.priority,
        ttl=message.ttl or 3600,
        encrypted=True,
        expires_at=expires_at
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Decrypt for response
    db_message.content = encryption_service.decrypt(db_message.content)
    return db_message


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: Session = Depends(get_db)):
    """Get a specific message"""
    db_message = db.query(Message).filter(Message.id == message_id).first()
    
    if not db_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    # Decrypt content
    db_message.content = encryption_service.decrypt(db_message.content)
    return db_message


@router.get("/device/{device_id}", response_model=MessageBatch)
async def get_device_messages(device_id: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get all messages for a device"""
    messages = db.query(Message).filter(Message.device_id == device_id).offset(skip).limit(limit).all()
    
    # Decrypt all messages
    for msg in messages:
        msg.content = encryption_service.decrypt(msg.content)
    
    total = db.query(Message).filter(Message.device_id == device_id).count()
    pending = db.query(Message).filter(Message.device_id == device_id, Message.status == MessageStatus.PENDING).count()
    delivered = db.query(Message).filter(Message.device_id == device_id, Message.status == MessageStatus.DELIVERED).count()
    failed = db.query(Message).filter(Message.device_id == device_id, Message.status == MessageStatus.FAILED).count()
    expired = db.query(Message).filter(Message.device_id == device_id, Message.status == MessageStatus.EXPIRED).count()
    
    return MessageBatch(
        total=total,
        pending=pending,
        delivered=delivered,
        failed=failed,
        expired=expired,
        messages=messages
    )


@router.patch("/{message_id}", response_model=MessageResponse)
async def update_message(message_id: int, update: MessageUpdate, db: Session = Depends(get_db)):
    """Update message status"""
    db_message = db.query(Message).filter(Message.id == message_id).first()
    
    if not db_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    db_message.status = update.status
    if update.delivered_at:
        db_message.delivered_at = update.delivered_at
    
    db.commit()
    db.refresh(db_message)
    
    # Decrypt content
    db_message.content = encryption_service.decrypt(db_message.content)
    return db_message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Delete a message"""
    db_message = db.query(Message).filter(Message.id == message_id).first()
    
    if not db_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    
    db.delete(db_message)
    db.commit()
    
    return None
