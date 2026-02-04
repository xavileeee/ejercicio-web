# GitHub Copilot / AI Agent Instructions for ejercicio-web ✅

## Quick overview
- Small FastAPI app that serves a static SPA and a minimal JSON API.
- Backend: `src/app.py` (FastAPI `app` instance). Static files are mounted at `/static`.
- Frontend: `src/static/` (HTML/JS/CSS) that calls the API at `/activities` and posts to `/activities/{activity_name}/signup`.
- Data is stored in-memory in `activities` (a dict keyed by activity name).

## What to know first (why things are structured this way) 💡
- The project is intentionally minimal for learning/demo: no DB, no auth, and no background workers. Changes should preserve the simplicity unless adding tests/features for learning.
- The frontend expects plain JSON endpoints and performs client-side rendering and encoding (see `src/static/app.js`).

## Key endpoints & data model (explicit examples) 🔧
- GET `/activities` → returns the full `activities` dict from `src/app.py`.
  - Example key: `"Chess Club"` with fields: `description`, `schedule`, `max_participants`, `participants` (list of emails).
- POST `/activities/{activity_name}/signup?email=...` → appends an email to `activities[activity_name]['participants']` and returns a confirmation message.
  - Note: activity name keys are case- and whitespace-sensitive (the frontend encodes them using `encodeURIComponent`).

## Project-specific behaviors & gotchas ⚠️
- In-memory state: all data resets on server restart. Do not expect persistence.
- The `signup` handler does NOT:
  - check `max_participants`,
  - prevent duplicate emails,
  - validate email format (beyond FastAPI type hinting in some cases).
  Be explicit about this when modifying handlers.
- `src/README.md` contains a slightly misleading run instruction (`python app.py`). Prefer `uvicorn src.app:app --reload` (see root `README.md`).

## Development & debugging workflows 🛠️
- Setup: create a venv and `pip install -r requirements.txt` (root `README.md`).
- Run locally (recommended):
  - `.venv/bin/uvicorn src.app:app --reload` (or `uvicorn src.app:app --reload` when venv activated)
  - Visit API docs: `http://localhost:8000/docs` and app UI: `http://localhost:8000/static/index.html`
- No unit tests exist yet; `pytest.ini` is present but empty of tests. If adding tests, keep them focused on the pure function-like handlers and simple e2e flows.

## Conventions and patterns to follow when editing code ✍️
- Keep the API surface small and explicit. Add endpoints into `src/app.py` and mirror minimal changes in the static UI when appropriate.
- Mutating global `activities` is the current pattern—if you introduce persistence, keep backward-compatible endpoints.
- Prefer small, self-contained PRs (example: add validation or capacity checks in `signup` without refactoring the entire data model).

## Useful files to reference 📁
- `src/app.py` — API and in-memory data model
- `src/static/app.js` — how the UI calls the endpoints (useful for examples and tests)
- `src/static/index.html` — the SPA entry
- `README.md` (root) — canonical run instructions

---

If anything above is unclear or you'd like more detail (e.g., suggested tests or a small example change), tell me which area to expand and I'll iterate. ✨
