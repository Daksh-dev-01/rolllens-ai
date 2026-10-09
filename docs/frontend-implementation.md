# Frontend implementation handoff

## Implemented
- Explore filters for name, relative name, voter ID, house number, age range, gender, polling station, and document version.
- Results with review status, model confidence, page reference, and evidence selection; pagination is present for API responses.
- Evidence panel with page image fallback, normalized percentage bounding-box overlay, invalid/missing-coordinate handling, extracted field values, and separate review/confidence semantics.
- Insights summary and age/gender aggregate charts based on the selected dataset response.
- Shared API service with environment-configured base URL and useful connection/status/JSON errors.
- Deterministic, clearly labeled synthetic demo fixtures.
- Tests for filters, empty states, bounding-box percentage scaling, invalid/missing boxes, and API errors.

## Integration dependencies
- Confirm the actual `RecordsResponse` envelope and field names with backend owner.
- Confirm document-page response/image URL and whether page images require authenticated or relative URLs.
- Confirm analytics summary schema and whether analytics can be scoped to a selected dataset/document. Current endpoint adapter consumes the summary endpoint response as returned; the UI labels its provided scope.
- Merge or replace the minimal shell only with Member 1's approval.

## Known limitations
- Review statuses are displayed, but this assigned scope does not implement review mutation actions.
- The document page image endpoint is read-only; demo fixtures intentionally have no source images, so the unavailable-image state is exercised.
- The starter ZIP's backend code, schema docs, and several frontend modules were zero-byte placeholders. Contracts in this frontend are explicit assumptions pending backend confirmation.
