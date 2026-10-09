# Data Dictionary

## Documents

| Field | Type | Meaning |
|---|---|---|
| `id` | string/UUID | Stable document identifier |
| `name` | string | Display name |
| `constituency` | string | Displayed jurisdiction/scope label |
| `versionLabel` | string | Human-readable version label in the frontend |
| `pageCount` | integer | Known page count |
| `recordCount` | integer | Number of extracted records, if known |
| `status` | enum | `READY`, `PROCESSING`, `NEEDS_ATTENTION`, `FAILED` |
| `origin` | enum | `SAMPLE` or `UPLOAD` |
| `updatedAt` | ISO timestamp | Last metadata/process update |
| `processedPages` | integer | Number of pages processed |
| `note` | nullable string | Human-readable processing or sample note |

The initial frontend document card uses camelCase. Backend schemas may use snake_case, but the adapter must map consistently.

## Voter records

| Field | Type | Meaning |
|---|---|---|
| `id` | string/UUID | Internal record identifier |
| `document_version_id` | string/UUID | Source document version |
| `serial_number` | nullable string | Printed serial number |
| `voter_id` | nullable string | Identifier extracted from source, when present |
| `name` | nullable string | Extracted name |
| `relative_name` | nullable string | Extracted relative name |
| `house_number` | nullable string | Extracted house number |
| `age` | nullable integer | Extracted age |
| `gender` | nullable string | Extracted value, if present and legible |
| `confidence` | nullable number | Model/extraction confidence, not verification |
| `review_status` | enum | `UNVERIFIED`, `VERIFIED`, `NEEDS_REVIEW` |
| `source.page_number` | integer | One-based page number |
| `source.bbox` | four numbers | Normalized `[x, y, width, height]` |

## Provenance rules

- Unknown values remain null.
- Do not infer a missing value from neighboring records.
- Keep model confidence separate from human verification.
- Corrections should be stored as review events with previous and new values.
- Preserve the original source file and source-page reference when permitted.
- Never use a person's name as a unique identifier.
- Synthetic fixtures must be labeled as synthetic.
