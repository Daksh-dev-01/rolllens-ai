from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.entities import Record, Page, FieldEvidence, DocumentVersion, Document
from app.services.search import search_records

router = APIRouter(prefix="/records", tags=["records"])

@router.get("")
def records(q: str | None = None, gender: str | None = None, min_age: int | None = Query(None, ge=0, le=120), max_age: int | None = Query(None, ge=0, le=120), verification_status: str | None = None, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    if min_age is not None and max_age is not None and min_age > max_age: raise HTTPException(422, "min_age cannot exceed max_age")
    if verification_status and verification_status not in {"unverified", "verified", "needs_review"}: raise HTTPException(422, "Invalid verification_status")
    result = search_records(db, q, gender, min_age, max_age, verification_status, page, page_size)
    items = []
    for r in result["items"]:
        source_page = db.get(Page, r.page_id)
        version = db.get(DocumentVersion, source_page.document_version_id) if source_page else None
        document = db.get(Document, version.document_id) if version else None
        items.append({"id":r.id,"external_id":r.external_id,"name":r.name,"age":r.age,"gender":r.gender,
          "house_number":r.house_number,"address":r.address,"extraction_confidence":r.extraction_confidence,
          "verification_status":r.verification_status,"bbox":r.bbox,"source":r.source,"page_id":r.page_id,
          "page_number":source_page.page_number if source_page else None,
          "document_id":document.id if document else None,"document_name":document.filename if document else None,
          "document_version":f"v{version.version_number}" if version else None})
    result["items"] = items
    return {"success": True, "data": result}

@router.get("/{record_id}")
def record_detail(record_id: str, db: Session = Depends(get_db)):
    r = db.get(Record, record_id)
    if not r: raise HTTPException(404, "Record not found")
    page = db.get(Page, r.page_id)
    version = db.get(DocumentVersion, page.document_version_id) if page else None
    document = db.get(Document, version.document_id) if version else None
    evidence = db.scalars(select(FieldEvidence).where(FieldEvidence.record_id == r.id)).all()
    record = {"id":r.id,"external_id":r.external_id,"name":r.name,"age":r.age,"gender":r.gender,
      "house_number":r.house_number,"address":r.address,"extraction_confidence":r.extraction_confidence,
      "verification_status":r.verification_status,"bbox":r.bbox,"source":r.source,
      "document_id":document.id if document else None,"document_name":document.filename if document else None,
      "document_version":f"v{version.version_number}" if version else None,"page_number":page.page_number if page else None}
    return {"success":True,"data":{"record":record,"source_page":{"page_id":page.id if page else None,"page_number":page.page_number if page else None,"width":page.width if page else None,"height":page.height if page else None,"document_id":document.id if document else None},
      "field_evidence":[{"field_name":e.field_name,"source_text":e.source_text,"bbox":e.bbox,"confidence":e.confidence} for e in evidence]}}
