# RollLens AI backend

A modular FastAPI backend for document upload, PDF page extraction/rendering, searchable records, aggregate analytics, and human review audit events. Demo rows are explicitly synthetic and never represent actual voters.

## Run locally (Python 3.11+)

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate ; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

By default, `ROLLLENS_DATABASE_URL` uses a local SQLite database for an easy deterministic demo. For PostgreSQL, copy `.env.example` to `.env`, create the database, and set `ROLLLENS_DATABASE_URL`. Uploads are stored under `private_uploads/`, outside the frontend's public directory. Set `ROLLLENS_DEMO_MODE=false` to disable seed data.

## Endpoints

- `GET /api/v1/health`
- `POST /api/v1/documents` multipart field `file` (PDF only)
- `GET /api/v1/documents`
- `GET /api/v1/documents/{document_id}/pages/{page_number}/image`
- `GET /api/v1/records?q=&gender=&min_age=&max_age=&verification_status=&page=&page_size=`
- `GET /api/v1/records/{record_id}`
- `GET /api/v1/analytics`
- `POST /api/v1/reviews` with `record_id`, `action` (`verify`, `unverify`, `flag`, `note`), optional reviewer/note/changes
- `GET /api/v1/reviews?record_id=&limit=`

All JSON routes return `{success, data}` on success and `{success, error}` on errors. Bounding boxes use normalized `[x, y, width, height]` coordinates. Extraction confidence is separate from verification status.

## Test

```bash
pytest -q
```

## Integration handoff / current limitations

The ingestion pipeline currently extracts page metadata and text, then persists pages. The AI extraction adapter is intentionally not fabricated: record extraction from uploaded PDFs is a handoff point for Member 4's structured extraction adapter. Until wired, use the synthetic seeded dataset for a deterministic demo. Comparison and safe-query services remain owned by Member 4 and are not registered here to avoid duplicate routes or circular imports. The local storage adapter can later be replaced behind the same interface.
