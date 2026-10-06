from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    type = Column(String, nullable=False, index=True) 
    # NEW_ORDER, ORDER_ACCEPTED, ORDER_STARTED, ORDER_DELIVERED, 
    # REVISION_REQUESTED, ORDER_COMPLETED, NEW_MESSAGE, NEW_REVIEW, 
    # SERVICE_APPROVED, SERVICE_REJECTED
    
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    user = relationship("User")
