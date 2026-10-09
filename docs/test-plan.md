# Test Plan

## Frontend checks

Run from `frontend/`:

```bash
npm run typecheck
npm run build
```

### Shell and navigation
- [ ] `/` redirects to `/documents`.
- [ ] All five main routes render inside one shell.
- [ ] Unknown routes redirect to Documents.
- [ ] Demo-mode banner is visible when `VITE_DEMO_MODE=true`.
- [ ] Layout remains usable at desktop and mobile widths.
- [ ] Keyboard focus indicators are visible.

### Documents page
- [ ] Loading state appears before the library is available.
- [ ] Seeded documents display expected metadata.
- [ ] Search matches document name, constituency, version, and ID.
- [ ] Status filters work independently of search.
- [ ] Empty filter results offer a clear-filters action.
- [ ] Invalid file types are rejected.
- [ ] Files above 50 MB are rejected by the frontend guard.
- [ ] Demo upload is explicitly labeled as simulated and does not call the backend.
- [ ] API failures show a useful message and retry action.
- [ ] Buttons and file input have accessible labels.

## Backend checks (assigned to Members 3 and 4)

- [ ] Health endpoint responds.
- [ ] Database setup and seeding are repeatable.
- [ ] Upload validation rejects invalid content and unsafe filenames.
- [ ] Search filters and pagination are validated.
- [ ] Unknown extraction fields remain null.
- [ ] Bounding boxes are normalized and validated.
- [ ] Analytics reflect the selected dataset.
- [ ] Query service rejects write operations and unsupported tables/fields.
- [ ] Version comparison handles ambiguous matching conservatively.
- [ ] Review events preserve an audit trail.

## End-to-end release checks

- [ ] Search result opens its correct source page.
- [ ] Bounding box remains aligned when the page image resizes.
- [ ] Loading, empty, and error states are understandable.
- [ ] The demo runs without a live AI provider.
- [ ] No real voter data or credentials appear in fixtures or logs.
- [ ] All demo actions have been rehearsed on the presentation device.
