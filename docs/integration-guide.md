# Integration Guide

## Goal

Integrate four independently developed modules into one RollLens AI application without duplicating the app shell, API client, route map, or data contracts.

## Before coding

1. Read `architecture.md` and `api-contracts.md`.
2. Confirm record status values, API envelope, coordinate convention, and error shape.
3. Create a small synthetic fixture with known source coordinates.
4. Keep the default frontend demo mode runnable.

## Branch and ownership workflow

- `main` should remain demo-ready.
- Each member works on a feature branch and opens a small pull request.
- Member 1 coordinates route and contract changes.
- Member 2 owns Explore, evidence viewer, Insights, and frontend tests.
- Member 3 owns database, ingestion, rendering, search, and analytics APIs.
- Member 4 owns extraction adapter, safe query service, and comparison logic.
- Avoid simultaneous edits to shared contracts or app-shell files.

## Integration order

1. Merge the shell and Documents page.
2. Merge backend health, seed data, and document listing.
3. Integrate Explore against mock data, then backend search.
4. Connect record detail and source-page evidence.
5. Connect aggregate analytics.
6. Connect the AI query and comparison modules.
7. Integrate review persistence and audit history.
8. Run all smoke tests and rehearse the demo.

## Local frontend setup

```bash
cd frontend
npm install
npm run dev
```

Default sample mode requires no backend. Set `VITE_DEMO_MODE=false` only when the API routes and response contracts are implemented.

## Pull request checklist

- [ ] Scope stays within the member's ownership.
- [ ] Contract changes are documented and communicated.
- [ ] `npm run typecheck` and `npm run build` pass for frontend changes.
- [ ] Backend tests pass for backend changes.
- [ ] Sample mode remains usable.
- [ ] No secrets or real electoral records are committed.
- [ ] Limitations and test results are included in the handoff.
