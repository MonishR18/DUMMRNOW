from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    provider = Column(String, nullable=False) # e.g. "stripe", "paypal"
    provider_transaction_id = Column(String, unique=True, index=True, nullable=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="PENDING", index=True) # PENDING, AUTHORIZED, PAID, FAILED, REFUNDED
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    order = relationship("Order", back_populates="payments")
