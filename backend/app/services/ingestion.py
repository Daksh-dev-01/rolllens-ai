from sqlalchemy.orm import Session
from app.models.entities import Document, DocumentVersion, Page
from app.services.rendering import inspect_pdf

def ingest_document(db: Session, document: Document):
    document.status = "processing"
    db.flush()
    pages = inspect_pdf(__import__('pathlib').Path(document.stored_path))
    version = DocumentVersion(document_id=document.id, version_number=1, is_active=True)
    db.add(version); db.flush()
    for p in pages:
        db.add(Page(document_version_id=version.id, page_number=p["page_number"], width=p["width"], height=p["height"], text=p["text"]))
    document.page_count = len(pages); document.status = "ready"
    db.commit()
    return document
