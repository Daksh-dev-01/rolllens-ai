# RollLens AI — Evidence Desk

RollLens AI is a hackathon prototype for evidence-first civic document intelligence. It is designed to turn scanned electoral-roll PDFs into structured records, connect results to their source pages, and support aggregate research and version comparison.

**This repository currently contains the Member 1 product shell and Documents page, plus route placeholders for the modules owned by other team members.** It is not yet a complete end-to-end backend/AI implementation.

## What is implemented in this slice

- Evidence Desk visual system and responsive application shell.
- Navigation for Documents, Explore, Insights, Compare, and Review.
- Documents library with loading, error, empty, and ready states.
- Document search and status filters.
- Seeded synthetic sample documents.
- PDF-only file selection, 50 MB frontend guard, and drag-and-drop affordance.
- Explicit demo-mode behavior: adding a file creates a simulated row only; no file is uploaded or processed.
- Shared frontend API client and typed document model.
- Architecture and API contract documentation.

The other four pages are intentional handoff placeholders until the corresponding team modules are integrated.

## Requirements

- Node.js 20 or newer (recommended)
- npm 10 or newer
- Git

A running backend and live AI credentials are **not required** for the default frontend demo.

## Run the frontend

Open a terminal in `frontend/`:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite (normally `http://localhost:5173`).

For a production build:

```bash
npm run typecheck
npm run build
npm run preview
```

> The package lock is intentionally not checked in yet. Run `npm install` to generate a lockfile after dependencies are resolved in your environment, then commit the generated lockfile once the team agrees on dependency versions.

## Demo configuration

The root `.env.example` documents shared environment variables. Vite only exposes variables prefixed with `VITE_`.

To use the default local demo, create `frontend/.env.local`:

```dotenv
VITE_DEMO_MODE=true
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Restart Vite after changing environment variables.

In demo mode:
- The library uses synthetic sample metadata.
- Adding a PDF is simulated in the browser.
- The selected file is not sent to a backend and is not processed.
- Sample and simulated content is labeled in the UI.
- No live AI provider is called.

To connect to a backend later, set `VITE_DEMO_MODE=false` and ensure the API implements the contracts in `docs/api-contracts.md`. The current Documents page expects `GET /documents` and `POST /documents` to return the documented document shape inside a `data` envelope. Confirm snake_case/camelCase mapping in the API adapter before integrating a backend.

## Project layout

```text
rolllens-ai/
├── docs/
│   ├── architecture.md
│   ├── api-contracts.md
│   ├── data-dictionary.md
│   ├── integration-guide.md
│   ├── demo-script.md
│   └── test-plan.md
├── frontend/
│   ├── src/
│   │   ├── components/layout/
│   │   ├── components/shared/
│   │   ├── mocks/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── styles/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
├── backend/                 # Assigned to Members 3 and 4
├── sample_data/
└── scripts/
```

## Team ownership

| Member | Scope |
|---|---|
| 1 — Integration owner | Application shell, routes, design system, Documents page, contracts, README, integration |
| 2 — Frontend explorer | Explore/search, evidence viewer, Insights, frontend tests |
| 3 — Backend | FastAPI, database, ingestion, rendering, search, analytics, review persistence |
| 4 — AI and comparison | AI provider adapter, schema validation, safe queries, version comparison |

Keep module ownership explicit. Coordinate changes to shared contracts before editing them. Do not create a second React app or duplicate API client.

## Integration sequence

1. Confirm shared data types and response envelope in `docs/api-contracts.md`.
2. Start the frontend and confirm all navigation routes load.
3. Integrate Member 2's search and evidence components against mock fixtures.
4. Integrate Member 3's API and seed data.
5. Integrate Member 4's safe query and comparison endpoints.
6. Run smoke tests and end-to-end demo rehearsal.
7. Freeze features and fix critical issues.

## Environment variables

| Variable | Used by | Purpose |
|---|---|---|
| `VITE_DEMO_MODE` | Frontend | `true` uses local synthetic data; `false` calls the API |
| `VITE_API_BASE_URL` | Frontend | API base path, default `http://localhost:8000/api/v1` |
| `DATABASE_URL` | Backend | PostgreSQL connection |
| `AI_PROVIDER` | Backend | AI adapter selection, default should be `mock` for demo |
| `AI_BASE_URL` | Backend | Optional model service URL |
| `AI_MODEL` | Backend | Exact configured model identifier |
| `UPLOAD_DIR` | Backend | Local document storage directory |
| `MAX_UPLOAD_MB` | Backend | Server-side upload limit |

Do not commit `.env` files, API keys, real electoral records, or uploaded source documents.

## Safety and data integrity

- Use synthetic data for demos and tests.
- A document being listed does not mean its extracted records are verified.
- Keep model confidence separate from human verification status.
- Preserve original source evidence and correction history.
- Natural-language queries must be read-only, restricted, and parameterized.
- Version differences and anomalies are review leads, not proof of misconduct.
- Before real deployment, add authentication, authorization, audit logging, appropriate retention controls, and a legal/privacy review.

## Known limitations in this slice

- Backend files in the starter archive may still be unimplemented.
- Explore, Insights, Compare, and Review are placeholders pending team integration.
- The simulated upload does not read or parse the selected PDF.
- Sample document counts are illustrative and must not be represented as official data.
- Production authentication, authorization, database migrations, and live AI inference are not included in the Member 1 scope.

## Demo walkthrough

1. Start the frontend.
2. Confirm the `DEMO MODE` indicator is visible.
3. Browse the seeded document library and filter by status.
4. Search for a document name or constituency.
5. Add a small PDF to demonstrate the simulated-upload disclosure.
6. Explain that the next integrated workflow will connect a record to its source page and bounding-box evidence.
7. Do not present simulated uploads as real extraction.

## Contribution checklist

- [ ] Read the architecture and API contracts.
- [ ] Keep changes within assigned ownership or coordinate first.
- [ ] Run `npm run typecheck` and `npm run build` for frontend changes.
- [ ] Add or update tests for changed behavior.
- [ ] Do not commit secrets or real voter data.
- [ ] Document any contract change and its impact on other modules.
