# AI extraction, safe queries, and version comparison

## Extraction adapter
`app.ai.base.ExtractionProvider` defines an async `extract(page_image: bytes, metadata: PageMetadata)` contract. Implementations return `VoterRecord` objects. `validate_records` is the strict provider boundary: unknown fields are forbidden, normalized boxes must remain within the page, confidence must be in [0,1], page numbers must match, and provider provenance must match configuration. `status=missing` or `status=illegible` should be used rather than guessing. Confidence means model-estimated visual certainty, not verified truth.

Set `ROLLLENS_AI_PROVIDER=mock` for deterministic, credential-free demos. Mock data is explicitly marked `provenance=mock` and is not OCR of the provided image. Live mode is intentionally not enabled by default. `openai-compatible`, `vllm`, and `ollama` currently fail closed unless all of `ROLLLENS_AI_BASE_URL`, `ROLLLENS_AI_MODEL`, and `ROLLLENS_AI_API_KEY` are configured; the endpoint-specific image payload must still be implemented and tested before enabling inference. Do not assume a Gemma model tag, runtime compatibility, GPU capacity, or API schema: verify the exact model artifact and its runtime documentation in the deployment environment.

## Safe query API
`POST /api/v1/queries` accepts `question`, optional `document_id`, and optional `version_id`. The deterministic planner supports record counts, age-group distribution, and unverified-record counts. It never executes generated SQL: each approved plan maps to a fixed parameterized statement against `voter_records`. Queries are aggregate-only, bounded, and use PostgreSQL transaction-local statement timeout. Confirm the table/column names against Member 3's schema before integration. Unsupported questions and individual-level requests return 422.

## Version comparison API
`POST /api/v1/versions/compare` accepts old/new version IDs and record fixtures. Match order is unique stable voter ID, then unique serial number as a low-confidence candidate. No name-only fuzzy matching is used. Unmatched records are additions/removals; duplicates or ambiguous identifiers are flagged for review. All modifications retain old/new values and source page references when supplied. Changes are candidate differences, never proof of identity or wrongdoing.

## Integration / handoff
- Include `queries.router` and `versions.router` under `/api/v1`; this module does not create a second application in the integration host.
- Use `app.db.session.get_db` or replace it with the project's shared dependency during integration.
- The query SQL assumes `voter_records(document_id, version_id, age, review_status)`. Align names with Member 3 before using the query endpoint against production data.
- Live inference is not production-ready until the chosen model identifier, image-input API, runtime, authentication, timeout/retry behavior, and target hardware are verified.
