from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models.entities import Record, Page, DocumentVersion, Document

def search_records(db: Session, q=None, gender=None, min_age=None, max_age=None, verification_status=None, page=1, page_size=20):
    stmt = select(Record).join(Page, Record.page_id == Page.id).join(DocumentVersion, Page.document_version_id == DocumentVersion.id).join(Document, DocumentVersion.document_id == Document.id).where(DocumentVersion.is_active.is_(True))
    if q:
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(or_(Record.name.ilike(pattern), Record.external_id.ilike(pattern), Record.house_number.ilike(pattern), Record.address.ilike(pattern)))
    if gender: stmt = stmt.where(Record.gender == gender)
    if min_age is not None: stmt = stmt.where(Record.age >= min_age)
    if max_age is not None: stmt = stmt.where(Record.age <= max_age)
    if verification_status: stmt = stmt.where(Record.verification_status == verification_status)
    total = len(db.scalars(stmt).all())
    items = db.scalars(stmt.order_by(Record.id).offset((page-1)*page_size).limit(page_size)).all()
    return {"items": items, "page": page, "page_size": page_size, "total": total}
