from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from core.database import get_db
from models.order import Order, OrderStatus
from models.service import Service
from schemas.order import OrderResponse
from schemas.service import ServiceResponse
from core.security import get_current_active_user, require_role
from models.user import User

router = APIRouter(prefix="/api/seller", tags=["seller"])


@router.get("/services", response_model=List[ServiceResponse])
def get_seller_services(db: Session = Depends(get_db), current_user: User = Depends(require_role(["PROVIDER"]))):
    return db.query(Service).filter(Service.seller_id == current_user.id).order_by(desc(Service.created_at)).all()


@router.get("/dashboard")
def get_seller_dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_role(["PROVIDER"]))):
    orders = db.query(Order).filter(Order.seller_id == current_user.id).all()
    services = db.query(Service).filter(Service.seller_id == current_user.id).all()
    active = [o for o in orders if o.status not in {OrderStatus.COMPLETED, OrderStatus.CANCELLED, OrderStatus.REFUNDED}]
    completed = [o for o in orders if o.status == OrderStatus.COMPLETED]
    delivered = [o for o in orders if o.status == OrderStatus.DELIVERED]
    pending = [o for o in orders if o.status == OrderStatus.PENDING]

    revenue = round(sum(o.amount for o in completed), 2)
    return {
        "revenue": revenue,
        "orders": len(orders),
        "active_orders": len(active),
        "completed_orders": len(completed),
        "pending_orders": len(pending),
        "delivered_orders": len(delivered),
        "services": len(services),
        "views": sum(s.view_count for s in services),
        "rating": current_user.rating or 0,
        "reviews": sum(s.review_count for s in services),
    }


@router.get("/analytics")
def get_seller_analytics(db: Session = Depends(get_db), current_user: User = Depends(require_role(["PROVIDER"]))):
    orders = db.query(Order).filter(Order.seller_id == current_user.id).all()
    return {
        "total_revenue": round(sum(o.amount for o in orders if o.status == OrderStatus.COMPLETED), 2),
        "total_orders": len(orders),
        "active_orders": len([o for o in orders if o.status not in {OrderStatus.COMPLETED, OrderStatus.CANCELLED, OrderStatus.REFUNDED}]),
        "completed_orders": len([o for o in orders if o.status == OrderStatus.COMPLETED]),
        "pending_orders": len([o for o in orders if o.status == OrderStatus.PENDING]),
        "delivered_orders": len([o for o in orders if o.status == OrderStatus.DELIVERED]),
    }


@router.get("/revenue")
def get_seller_revenue(db: Session = Depends(get_db), current_user: User = Depends(require_role(["PROVIDER"]))):
    completed = db.query(Order).filter(Order.seller_id == current_user.id, Order.status == OrderStatus.COMPLETED).all()
    return {
        "total_revenue": round(sum(o.amount for o in completed), 2),
        "monthly_revenue": round(sum(o.amount for o in completed), 2),
        "orders": len(completed),
    }


@router.get("/orders", response_model=List[OrderResponse])
def get_seller_orders(db: Session = Depends(get_db), current_user: User = Depends(require_role(["PROVIDER"]))):
    return db.query(Order).filter(Order.seller_id == current_user.id).order_by(desc(Order.created_at)).all()
