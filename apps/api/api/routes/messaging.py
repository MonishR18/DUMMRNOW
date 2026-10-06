from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from core.database import get_db
from models.messaging import Conversation, Message
from models.order import Order
from schemas.messaging import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse
from core.security import get_current_active_user
from models.user import User

router = APIRouter(prefix="/api/conversations", tags=["messaging"])

@router.get("", response_model=List[ConversationResponse])
def get_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return db.query(Conversation).filter((Conversation.buyer_id == current_user.id) | (Conversation.seller_id == current_user.id)).all()

@router.post("", response_model=ConversationResponse)
def create_conversation(conv: ConversationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    participant = db.query(User).filter(User.id == conv.participant_id).first()
    if not participant:
        raise HTTPException(status_code=400, detail="Participant not found")
        
    # Check if conversation already exists
    existing = db.query(Conversation).filter(
        or_(
            (Conversation.buyer_id == current_user.id) & (Conversation.seller_id == participant.id),
            (Conversation.seller_id == current_user.id) & (Conversation.buyer_id == participant.id)
        )
    ).first()
    if existing:
        return existing
        
    db_conv = Conversation(
        buyer_id=current_user.id,
        seller_id=participant.id,
        order_id=conv.order_id
    )
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conv.buyer_id != current_user.id and conv.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return conv

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conv.buyer_id != current_user.id and conv.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
def send_message(conversation_id: int, msg: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conv.buyer_id != current_user.id and conv.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    db_msg = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=msg.content
    )
    db.add(db_msg)
    
    # Notify the other participant
    other_id = conv.seller_id if current_user.id == conv.buyer_id else conv.buyer_id
    from models.notification import Notification
    db_notif = Notification(user_id=other_id, type="NEW_MESSAGE", title="New Message", message=f"You received a new message")
    db.add(db_notif)
    
    db.commit()
    db.refresh(db_msg)
    return db_msg
