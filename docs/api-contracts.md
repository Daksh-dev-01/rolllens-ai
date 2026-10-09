# RollLens AI — API Contracts (v1)

This document is the shared source of truth for frontend/backend integration. Update this file before changing a field name or response shape.

## 1. Base URL and response envelope

Base path: `/api/v1`

Successful responses:

```json
{
  "data": {},
  "meta": {
    "request_id": "request-001"
  }
}
```

Error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The supplied filter is invalid."
  },
  "meta": {
    "request_id": "request-001"
  }
}
```

The frontend client unwraps the `data` property. Endpoint schemas below describe the contents of `data`.

## 2. Shared types

```ts
export type DocumentStatus =
  | "READY"
  | "PROCESSING"
  | "NEEDS_ATTENTION"
  | "FAILED";

export type DocumentOrigin = "SAMPLE" | "UPLOAD";

export type ReviewStatus =
  | "UNVERIFIED"
  | "VERIFIED"
  | "NEEDS_REVIEW";

export interface RollDocument {
  id: string;
  name: string;
  constituency: string;
  versionLabel: string;
  pageCount: number;
  recordCount: number;
  status: DocumentStatus;
  origin: DocumentOrigin;
  updatedAt: string;
  processedPages: number;
  note?: string;
}

export interface SourceEvidence {
  page_number: number;
  image_url?: string;
  bbox: [number, number, number, number];
}

export interface VoterRecord {
  id: string;
  document_version_id: string;
  name: string | null;
  relative_name: string | null;
  voter_id: string | null;
  house_number: string | null;
  age: number | null;
  gender: string | null;
  confidence: number | null;
  review_status: ReviewStatus;
  source: SourceEvidence;
}
```

`RollDocument` uses camelCase in the initial frontend model for its library cards. Backend Pydantic models may use snake_case; the API adapter must explicitly map names if needed. Do not mix naming conventions inside a single response.

## 3. Health

`GET /health`

Response `data`:

```json
{
  "status": "ok",
  "mode": "demo"
}
```

The backend owner may expose this at `/api/v1/health` instead; choose one path before backend implementation and keep README/tests consistent. Recommended final route: `GET /api/v1/health`.

## 4. Documents

### List documents

`GET /documents`

Response `data`: `RollDocument[]`

### Upload a PDF

`POST /documents`

Content type: `multipart/form-data`, field name `file`.

Response `data`: one `RollDocument`.

Requirements:
- PDF only.
- Configurable size limit; initial frontend limit is 50 MB.
- Validate content and file metadata on the server.
- Do not make a successful response imply extraction is complete unless status is `READY`.

### Page evidence

`GET /documents/{document_id}/pages/{page_number}`

Response `data`:

```json
{
  "document_id": "doc-001",
  "page_number": 1,
  "image_url": "/api/v1/documents/doc-001/pages/1/image",
  "status": "READY"
}
```

Page image URLs must be access-controlled. Do not expose local filesystem paths.

## 5. Record search and detail

`GET /records`

Suggested query parameters:
- `q`: text query
- `voter_id`
- `name`
- `relative_name`
- `house_number`
- `age_min`
- `age_max`
- `gender`
- `document_version_id`
- `page`
- `limit`

Response `data`:

```json
{
  "items": [],
  "page": 1,
  "limit": 20,
  "total": 0
}
```

`GET /records/{record_id}` returns one `VoterRecord`, including its source evidence. Unknown values remain `null`; do not guess missing fields.

## 6. Analytics

`GET /analytics/summary`

Suggested parameters: `document_version_id` or an agreed list of version IDs.

Response `data`:

```json
{
  "scope": "Selected sample version",
  "total_records": 0,
  "age_groups": [],
  "gender_distribution": [],
  "unverified_count": 0,
  "caveats": []
}
```

All aggregates must be calculated from the selected dataset. Do not fabricate metrics or present aggregate statistics as claims about individual behavior.

## 7. Natural-language queries

`POST /queries`

Request:

```json
{
  "question": "How many records are in this sample?",
  "document_version_ids": ["version-001"]
}
```

Response `data`:

```json
{
  "answer": "Example response based on the selected dataset.",
  "scope": "version-001",
  "result_table": {
    "columns": ["metric", "value"],
    "rows": [["record_count", 0]]
  },
  "caveats": ["Illustrative response shape; values must come from query results."]
}
```

Only allow read-only, validated queries against approved tables/columns. Never execute arbitrary model-generated SQL without validation.

## 8. Version comparison

`POST /versions/compare`

Request:

```json
{
  "old_version_id": "version-old",
  "new_version_id": "version-new"
}
```

Response `data`:

```json
{
  "summary": {
    "added": 0,
    "removed": 0,
    "modified": 0,
    "needs_review": 0
  },
  "changes": []
}
```

Every change should include category, record references, source evidence references, and uncertainty/review state. Differences are candidates for review, not proof of wrongdoing.

## 9. Review workflow

`GET /reviews?status=NEEDS_REVIEW`

`POST /reviews`

Request:

```json
{
  "record_id": "record-001",
  "field_name": "name",
  "old_value": "Extracted value",
  "new_value": "Corrected value",
  "note": "Compared against the source image."
}
```

Persist an audit event with reviewer identity when authentication exists. Do not overwrite the only copy of the original extraction.

## 10. Error codes

Recommended codes:
- `VALIDATION_ERROR`
- `NOT_FOUND`
- `UNSUPPORTED_FILE_TYPE`
- `FILE_TOO_LARGE`
- `PROCESSING_FAILED`
- `QUERY_NOT_ALLOWED`
- `RATE_LIMITED`
- `INTERNAL_ERROR`

## 11. Contract rules

1. Frontend mock fixtures must follow these shapes.
2. Backend Pydantic schemas must validate the same semantics.
3. Coordinate order is `[x, y, width, height]`, normalized from 0 to 1.
4. Extraction confidence and human review status are separate.
5. Any breaking change requires updating this file and relevant tests in the same PR.
