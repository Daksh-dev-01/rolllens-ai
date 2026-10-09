from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.analytics import aggregate
router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("")
def analytics(db: Session = Depends(get_db)):
    return {"success": True, "data": aggregate(db)}
