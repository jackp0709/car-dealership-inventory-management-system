# Car Dealership Inventory Management System

A full-stack web application for dealership employees to manage vehicle inventory, process vehicle purchases, manage users, and monitor dealership statistics.

## Technology stack

- Backend: FastAPI and Python 3.12+
- Frontend: React, Vite, Material UI, React Router, and Axios
- Database (planned): PostgreSQL with SQLAlchemy and Alembic

## Project structure

```text
backend/    FastAPI application
frontend/   React application
docs/       Project architecture and planning documents
prompts/    Development prompts
```

## Run the backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

The health check is available at `http://127.0.0.1:8000/health`.

## Run the frontend

```powershell
cd frontend
npm install
npm run dev
```

## Current status

Sprint 01 is limited to project initialization. Authentication, persistence, APIs, and application pages are intentionally deferred to later sprints.
