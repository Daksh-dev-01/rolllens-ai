from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.entities import Record, ReviewEvent
router = APIRouter(prefix="/reviews", tags=["reviews"])
class ReviewInput(BaseModel):
    record_id: str
    action: str = Field(pattern="^(verify|unverify|flag|note)$")
    reviewer: str = Field(default="anonymous", max_length=120)
    note: str | None = Field(default=None, max_length=2000)
    changes: dict | None = None
@router.post("")
def submit_review(payload: ReviewInput, db: Session = Depends(get_db)):
    record = db.get(Record, payload.record_id)
    if not record: raise HTTPException(404, "Record not found")
    if payload.action in {"verify", "unverify", "flag"}:
        record.verification_status = {"verify":"verified", "unverify":"unverified", "flag":"needs_review"}[payload.action]
    event = ReviewEvent(record_id=record.id, reviewer=payload.reviewer, action=payload.action, note=payload.note, changes=payload.changes)
    db.add(event); db.commit(); db.refresh(event)
    return {"success":True,"data":{"id":event.id,"record_id":event.record_id,"action":event.action,"verification_status":record.verification_status}}
@router.get("")
def list_reviews(record_id: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    if limit < 1 or limit > 500: raise HTTPException(422, "limit must be between 1 and 500")
    stmt = select(ReviewEvent).order_by(ReviewEvent.created_at.desc()).limit(limit)
    if record_id: stmt = stmt.where(ReviewEvent.record_id == record_id)
    rows = db.scalars(stmt).all()
    return {"success":True,"data":[{"id":r.id,"record_id":r.record_id,"reviewer":r.reviewer,"action":r.action,"note":r.note,"changes":r.changes,"created_at":r.created_at} for r in rows]}
