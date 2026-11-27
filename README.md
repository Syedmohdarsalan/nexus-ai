# NEXUS AI
The Intelligent Financial Operations & Autonomous Payment Platform.

Phase 1.1: tested backend foundation, using synthetic invoices only. No real payments or Visa integration. Local development only; do not expose this unauthenticated API publicly.

## Windows setup (PowerShell)
Install Python 3.12 or 3.13, Git and VS Code. Open this folder in VS Code. From the root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The commands use the virtual environment's Python directly so PowerShell script execution policy need not be changed. On macOS/Linux, substitute `.venv/bin/python` for the Windows path.

Open http://127.0.0.1:8000/docs in your browser. Click POST /api/v1/invoices, Try it out, and paste:

```json
{"invoice_number":"INV-001","vendor_name":"Demo Cloud Services","amount_minor":2500000,"currency":"INR","due_date":"2026-12-15"}
```

Expected: HTTP 201, generated ID and pending_review status. GET /api/v1/invoices returns the saved record. Repeating the same vendor/invoice pair returns HTTP 409. A negative amount returns HTTP 422. Stop the server with Ctrl+C.

## First commit
Run from the repository root, after reviewing the code:

```powershell
git init -b main
git add .
git commit -m "Initialize FastAPI backend and invoice database"
```

Create an empty GitHub repository named nexus-ai if you want to push it. Copy its remote URL and use `git remote add origin YOUR_REPOSITORY_URL`, then `git push -u origin main`. Never commit credentials or actual financial data.

## Layout
- backend/app: application entry point, database, models, validation, invoice endpoints
- backend/alembic: versioned database migration
- backend/tests: automated API tests
- frontend: placeholder for future React UI
- data: example synthetic CSV; import is not implemented yet
- docs: scope and next steps

## Current limitations
No frontend, CSV import, fraud scoring, authentication, LLM, routing, approvals or payment execution. SQLite is the only database tested. PostgreSQL is planned. See docs/phase-1.md.
