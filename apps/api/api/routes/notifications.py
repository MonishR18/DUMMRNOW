from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from core.database import get_db
from models.notification import Notification
from schemas.notification import NotificationResponse
from core.security import get_current_active_user
from models.user import User

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.get("", response_model=List[NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return db.query(Notification).filter(Notification.user_id == current_user.id).order_by(desc(Notification.created_at)).all()

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notif.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif

@router.post("/read-all", status_code=status.HTTP_200_OK)
def read_all_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db.query(Notification).filter(Notification.user_id == current_user.id, Notification.is_read == False).update({"is_read": True})
    db.commit()
    return {"status": "ok"}
