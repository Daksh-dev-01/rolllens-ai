# RollLens AI — Architecture and Integration Boundaries

## 1. Product objective

RollLens AI is an evidence-first civic document intelligence workspace. It helps authorized researchers transform scanned electoral-roll PDFs into structured records, search those records, inspect their source evidence, and review aggregate patterns or differences between versions.

The product must preserve the distinction between:
- **Extracted:** a value was returned by a processing system.
- **Unverified:** a human has not checked the value against source evidence.
- **Verified:** an authorized reviewer has checked the value against the source.
- **Needs review:** a field or record needs further inspection.

An anomaly or version difference is an investigation lead, not proof of misconduct.

## 2. High-level architecture

```text
Researcher
    |
    v
React + Vite + TypeScript
  |-- Application shell / navigation
  |-- Documents page
  |-- Explore (Member 2)
  |-- Insights (Member 2)
  |-- Compare (Member 4)
  |-- Review (shared frontend/backend integration)
    |
    v
FastAPI /api/v1
  |-- Document ingestion and rendering (Member 3)
  |-- Search and record details (Member 3)
  |-- Aggregate analytics (Member 3)
  |-- AI extraction adapter (Member 4)
  |-- Read-only natural-language queries (Member 4)
  |-- Version comparison (Member 4)
    |
    +--> PostgreSQL
    +--> Local file storage for demo / optional object storage
    +--> Configurable AI provider
```

The hackathon implementation is a modular monolith. Do not introduce microservices unless a demonstrated need requires them.

## 3. Frontend shell (Member 1)

Owned paths:
- `frontend/src/App.tsx`
- `frontend/src/main.tsx`
- `frontend/src/routes/`
- `frontend/src/components/layout/`
- `frontend/src/components/shared/`
- `frontend/src/pages/DocumentsPage.tsx`
- `frontend/src/services/api.ts` and `rolllens.ts` are shared integration surfaces; coordinate edits.
- `docs/architecture.md`
- `docs/api-contracts.md`
- `README.md`

The shell owns route registration, global navigation, mode indication, visual tokens, the document library entry point, and integration coordination. It must not duplicate the Explore, Insights, extraction, query, or comparison implementations.

## 4. Team boundaries

| Member | Primary ownership | Must coordinate |
|---|---|---|
| 1 | Shell, route map, Documents page, shared UI, integration | Shared contracts and final merge |
| 2 | Explore, evidence viewer, Insights, frontend tests | Shared frontend API client and types |
| 3 | FastAPI, SQLAlchemy, document upload/rendering, search, analytics, review persistence | Schema, route registration, DB session |
| 4 | AI adapter/validation, safe query service, version comparison | Provider config, DB models, route registration |

No member should create a second application shell, duplicate a shared API client, or silently change a contract.

## 5. Demo mode

`VITE_DEMO_MODE=true` selects deterministic sample mode. The Documents page uses synthetic sample metadata. Adding a file in this mode is a **simulation only**: the selected file is not sent to a backend or processed, and the resulting row is labeled as a demo upload.

When `VITE_DEMO_MODE=false`, the frontend calls the configured backend at `VITE_API_BASE_URL`. A working backend and matching API response contracts are required. The initial Member 1 deliverable does not implement the backend.

Never describe sample data or simulated processing as live AI output.

## 6. Evidence coordinates

Bounding boxes use `[x, y, width, height]` in normalized page-image coordinates:
- Origin: top-left.
- Valid range for x/y: 0 through 1.
- Width and height: non-negative and must not extend beyond the image.
- The frontend scales normalized values to the rendered page image.

Store page number and coordinate-space information with the evidence. Model confidence and human verification status are separate fields.

## 7. Data and security boundaries

- Keep uploaded files in a non-public storage location.
- Validate file type, size, and filenames.
- Do not commit real electoral records, credentials, or local uploads.
- Keep database access on the backend.
- The query service must be read-only and constrained to approved tables and fields.
- Use parameterized queries and enforce result limits/timeouts.
- Minimize exposure of individual-level data and audit sensitive review actions.
- Use synthetic data for the default demonstration.
- Follow applicable privacy, data-use, and election-related requirements before any real deployment.

## 8. Build order

1. Confirm contracts and shared types.
2. Ensure frontend shell and backend health endpoint start.
3. Seed synthetic records and evidence assets.
4. Integrate Explore/search/evidence.
5. Integrate analytics and review.
6. Integrate query and version comparison.
7. Test failure paths and fallback behavior.
8. Freeze features and rehearse the demo.

## 9. Architecture decisions

- One frontend app and one FastAPI app.
- REST endpoints under `/api/v1`.
- JSON envelope for successful and error responses.
- Mock/sample mode must not require an AI provider.
- Database and AI provider are configured via environment variables.
- Optional infrastructure must not block the main demo workflow.
