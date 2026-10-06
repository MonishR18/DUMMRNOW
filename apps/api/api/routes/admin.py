from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.user import User
from models.service import Service
from models.order import Order, Review
from core.security import require_role

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_role(["ADMIN"]))):
    return {
        "users": db.query(User).count(),
        "services": db.query(Service).count(),
        "orders": db.query(Order).count(),
        "revenue": sum([o.amount for o in db.query(Order).all()])
    }

@router.get("/users")
def get_admin_users(db: Session = Depends(get_db), current_user: User = Depends(require_role(["ADMIN"]))):
    return db.query(User).all()

@router.get("/services")
def get_admin_services(db: Session = Depends(get_db), current_user: User = Depends(require_role(["ADMIN"]))):
    return db.query(Service).all()

@router.get("/orders")
def get_admin_orders(db: Session = Depends(get_db), current_user: User = Depends(require_role(["ADMIN"]))):
    return db.query(Order).all()

@router.get("/reviews")
def get_admin_reviews(db: Session = Depends(get_db), current_user: User = Depends(require_role(["ADMIN"]))):
    return db.query(Review).all()

@router.get("/reports")
def get_admin_reports(db: Session = Depends(get_db), current_user: User = Depends(require_role(["ADMIN"]))):
    return {
        "users": db.query(User).count(),
        "services": db.query(Service).count(),
        "orders": db.query(Order).count(),
        "reviews": db.query(Review).count(),
        "revenue": round(sum(o.amount for o in db.query(Order).all() if o.status == "COMPLETED"), 2),
    }
