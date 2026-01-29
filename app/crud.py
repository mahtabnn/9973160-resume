from sqlalchemy.orm import Session
from . import models, schemas

def create_request(db: Session, req: schemas.ProjectRequestCreate) -> models.ProjectRequest:
    db_item = models.ProjectRequest(
        name=req.name,
        email=req.email,
        description=req.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectRequest).order_by(models.ProjectRequest.created_at.desc()).offset(skip).limit(limit).all()

def get_request(db: Session, request_id: int) -> models.ProjectRequest | None:
    return db.query(models.ProjectRequest).filter(models.ProjectRequest.id == request_id).first()

def update_request(db: Session, request_id: int, update: schemas.ProjectRequestUpdate) -> models.ProjectRequest | None:
    db_item = get_request(db, request_id)
    if not db_item:
        return None
    if update.status is not None:
        db_item.status = update.status
    if update.admin_notes is not None:
        db_item.admin_notes = update.admin_notes
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_request(db: Session, request_id: int) -> bool:
    db_item = get_request(db, request_id)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True