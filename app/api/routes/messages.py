"""
API routes for messages
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from app.models import Message, MessageSchema, MessageCreateSchema
from app.services import encryption_service
from app.database import get_db

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageSchema)
async def create_message(
    message_data: MessageCreateSchema,
    db: Session = Depends(get_db)
):
    """
    Create a new message
    """
    try:
        # Generate unique ID
        message_id = str(uuid.uuid4())
        
        # Encrypt content if requested
        content = message_data.content
        is_encrypted = message_data.is_encrypted
        
        if is_encrypted:
            content = encryption_service.encrypt(content)
        
        # Create message record
        message = Message(
            id=message_id,
            device_id=message_data.device_id,
            content=content,
            is_encrypted=is_encrypted,
            rssi=message_data.rssi,
            snr=message_data.snr,
            frequency=message_data.frequency,
            data_rate=message_data.data_rate
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return message
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{message_id}", response_model=MessageSchema)
async def get_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a message by ID
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Decrypt if encrypted
    if message.is_encrypted:
        try:
            message.content = encryption_service.decrypt(message.content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")
    
    return message


@router.get("/device/{device_id}", response_model=List[MessageSchema])
async def get_device_messages(
    device_id: str,
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get all messages from a specific device
    """
    messages = db.query(Message).filter(
        Message.device_id == device_id
    ).order_by(Message.timestamp.desc()).offset(skip).limit(limit).all()
    
    # Decrypt encrypted messages
    for message in messages:
        if message.is_encrypted:
            try:
                message.content = encryption_service.decrypt(message.content)
            except Exception:
                pass
    
    return messages


@router.get("/", response_model=List[MessageSchema])
async def list_messages(
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    List all messages
    """
    messages = db.query(Message).order_by(
        Message.timestamp.desc()
    ).offset(skip).limit(limit).all()
    
    # Decrypt encrypted messages
    for message in messages:
        if message.is_encrypted:
            try:
                message.content = encryption_service.decrypt(message.content)
            except Exception:
                pass
    
    return messages


@router.delete("/{message_id}")
async def delete_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a message by ID
    """
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    db.commit()
    
    return {"detail": "Message deleted successfully"}
