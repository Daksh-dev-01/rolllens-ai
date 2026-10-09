# RollLens AI — merged project notes

This archive combines the four submitted ZIPs into one `rolllens-ai/` project. Duplicate files were resolved by keeping the non-empty implementation from the relevant module owner; generated Python caches, pytest cache files, and a checked-in local SQLite database were excluded. Frontend package metadata and the frontend API/service layer were merged, and the backend application now registers the documents, records, analytics, reviews, safe-query, and version-comparison routers together.

## Run

Frontend (Node.js 20+):

```bash
cd frontend
npm install
npm run dev
```

Backend (Python 3.11+):

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate ; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The frontend defaults to synthetic demo data; uploads are simulated in demo mode. The backend also seeds synthetic rows by default. Do not use demo fixtures as real records.

## Integration caveats

- The frontend's search API can pass only one free-text term to the current backend search endpoint; the demo supports the richer field-by-field filters. Relative-name and polling-station filtering are not represented in the current backend schema.
- The backend page-image endpoint returns image bytes; the frontend uses its direct URL in API mode. A deployment on a different origin needs appropriate CORS configuration.
- The comparison endpoint accepts supplied old/new record fixtures; it is not yet wired to fetch version records from the database.
- The AI adapter is deliberately fail-closed for live inference. Mock extraction is explicitly synthetic and does not OCR uploaded documents.
- The review and comparison pages remain UI handoff placeholders even though backend endpoints/services are included.
- Run the backend and frontend tests in the target environment after installing dependencies. Dependency installation and a full production build were not performed as part of archive merging.
