from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.service import ServicePackage, Service
from schemas.service import ServicePackageUpdate, ServicePackageResponse
from core.security import get_current_active_user
from models.user import User

router = APIRouter(prefix="/api/packages", tags=["packages"])

@router.patch("/{package_id}", response_model=ServicePackageResponse)
def update_package(package_id: int, package: ServicePackageUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_package = db.query(ServicePackage).filter(ServicePackage.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")
        
    service = db.query(Service).filter(Service.id == db_package.service_id).first()
    if service.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    update_data = package.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_package, key, value)
        
    db.commit()
    db.refresh(db_package)
    return db_package

@router.delete("/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package(package_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_package = db.query(ServicePackage).filter(ServicePackage.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")
        
    service = db.query(Service).filter(Service.id == db_package.service_id).first()
    if service.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db.delete(db_package)
    db.commit()
