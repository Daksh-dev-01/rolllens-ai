from sqlalchemy import select
from app.db.session import Base, engine, SessionLocal
from app.models.entities import Document, DocumentVersion, Page, Record

def seed():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        existing = db.scalar(select(Document).where(Document.sha256 == "synthetic-demo-dataset"))
        if existing: return
        doc = Document(filename="SYNTHETIC_DEMO_ONLY.pdf", stored_path="", sha256="synthetic-demo-dataset", status="ready", page_count=2)
        db.add(doc); db.flush()
        version = DocumentVersion(document_id=doc.id, version_number=1, is_active=True); db.add(version); db.flush()
        p1 = Page(document_version_id=version.id, page_number=1, width=595, height=842, text="Synthetic demo page — not real electoral data")
        p2 = Page(document_version_id=version.id, page_number=2, width=595, height=842, text="Synthetic demo page — not real electoral data")
        db.add_all([p1,p2]); db.flush()
        demo = [
            (p1, "DEMO-001", "Asha Example", 34, "female", "D-01"),
            (p1, "DEMO-002", "Ravi Sample", 42, "male", "D-02"),
            (p2, "DEMO-003", "Meera Fiction", 27, "female", "D-03"),
            (p2, "DEMO-004", "Kiran Placeholder", 56, "unknown", "D-04"),
        ]
        for page, ext, name, age, gender, house in demo:
            db.add(Record(page_id=page.id, external_id=ext, name=name, age=age, gender=gender, house_number=house, extraction_confidence=1.0, verification_status="unverified", bbox=[0.1,0.2,0.5,0.08], source="synthetic_demo"))
        db.commit()
if __name__ == "__main__": seed()
