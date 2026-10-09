from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.entities import Document, Page, DocumentVersion
from app.storage.local import save_upload
from app.services.ingestion import ingest_document
from app.services.rendering import render_page
from app.ai.base import PageMetadata
from app.ai.provider import get_provider
from pathlib import Path

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    path, digest, _ = await save_upload(file)
    doc = Document(filename=Path(file.filename).name, stored_path=str(path), sha256=digest, status="uploaded")
    try:
        db.add(doc); db.flush(); ingest_document(db, doc)
        return {"success": True, "data": {"id": doc.id, "filename": doc.filename, "status": doc.status, "page_count": doc.page_count}}
    except Exception as exc:
        db.rollback(); path.unlink(missing_ok=True)
        raise HTTPException(422, detail={"success": False, "error": {"code": "PDF_PROCESSING_FAILED", "message": str(exc)}})


@router.get("")
def list_documents(db: Session = Depends(get_db)):
    docs = db.scalars(select(Document).order_by(Document.created_at.desc())).all()
    return {"success": True, "data": [{"id": d.id, "filename": d.filename, "status": d.status, "page_count": d.page_count, "created_at": d.created_at} for d in docs]}


@router.get("/{document_id}/pages/{page_number}/image")
def page_image(document_id: str, page_number: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(404, "Document not found")
    try: data = render_page(Path(doc.stored_path), page_number)
    except ValueError as e: raise HTTPException(404, str(e))
    return Response(data, media_type="image/png", headers={"Cache-Control": "no-store"})


@router.post("/{document_id}/pages/{page_number}/extract")
async def extract_page(document_id: str, page_number: int, db: Session = Depends(get_db)):
    """Run configured AI extraction for one rendered page; results require human review."""
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    page = db.scalar(
        select(Page).join(DocumentVersion, Page.document_version_id == DocumentVersion.id)
        .where(DocumentVersion.document_id == document_id, Page.page_number == page_number)
    )
    if not page:
        raise HTTPException(404, "Page not found")
    try:
        image_bytes = render_page(Path(doc.stored_path), page_number)
        provider = get_provider()
        metadata = PageMetadata(
            document_id=doc.id,
            version_id=page.document_version_id,
            page_number=page.page_number,
        )
        records = await provider.extract(image_bytes, metadata)
    except RuntimeError as exc:
        raise HTTPException(502, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(503, str(exc)) from exc
    return {
        "success": True,
        "data": {
            "document_id": doc.id,
            "page_number": page.page_number,
            "records": [record.model_dump(mode="json") for record in records],
            "requires_human_review": True,
        },
    }
