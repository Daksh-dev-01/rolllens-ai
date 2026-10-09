# RollLens AI frontend — Explore, Evidence, Insights

## Run locally

Requirements: Node.js 20+ and npm.

```bash
cd frontend
npm install
npm run dev
```

The frontend starts in deterministic **synthetic demo mode** by default. The banner labels all fixture records as synthetic. No live AI credentials or backend are required.

To use the API instead, set `VITE_USE_MOCK_DATA=false` and optionally `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env.local`. The API base URL is intentionally environment-configured; do not hardcode deployment URLs. Expected endpoints are `GET /api/v1/records`, `GET /api/v1/records/{id}`, `GET /api/v1/documents/{id}/pages/{page}`, and `GET /api/v1/analytics`.

## Test and build

```bash
npm test
npm run build
```

Tests cover normalized bounding-box percentages and invalid/missing coordinates, filter behavior and empty results, and API error responses.

## Integration contract assumptions to confirm

- `GET /records` returns `{items, total, page, page_size}`; if the backend uses a different envelope, coordinate the response type with the integration and backend owners.
- Record fields use the documented names represented in `src/types/index.ts`; optional fields are handled as unavailable instead of fabricated.
- Page endpoint returns an object containing `image_url`. If the backend serves a binary/image response or uses another field, adapt `getPageEvidence` with Member 3.
- Analytics endpoint returns `total_records`, `age_groups: [{label,count}]`, `gender_distribution: [{label,count}]`, and optional dataset scope/name. These assumptions must be reconciled against the actual backend schema before switching off demo mode.
- Bounding boxes are treated as normalized `[x,y,width,height]` values. No coordinate conversion is performed. The viewer rejects boxes outside `[0,1]` image bounds.

The navigation shell in `src/App.tsx` is intentionally minimal because the supplied archive's app shell was empty. Coordinate with Member 1 before merging it into their shared shell and navigation.

## Clean install after receiving the project ZIP

The ZIP intentionally excludes platform-specific `node_modules` and Python virtual-environment folders. From this directory, run:

```powershell
npm install
npm test
npm run typecheck
npm run build
```

The frontend uses Vite 5 with Vitest 2 to keep the Vite/Vitest type definitions aligned. Demo mode uses clearly labeled synthetic records; uploads in demo mode are simulated and do not process a real PDF.
