from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.user import UserResponse

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    sender_id: int
    is_read: bool
    created_at: datetime
    
    sender: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    order_id: Optional[int] = None

class ConversationCreate(ConversationBase):
    participant_id: int # The other user to chat with, backend figures out buyer/seller

class ConversationResponse(ConversationBase):
    id: int
    buyer_id: int
    seller_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    buyer: Optional[UserResponse] = None
    seller: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True
