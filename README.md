# Car Dealership Inventory Management System

A full-stack application for managing dealership inventory, vehicle acquisitions, sales, staff users, and an operational dashboard.

## Features

- JWT-authenticated Admin and Employee access
- Vehicle inventory management with VIN validation and available/sold lifecycle rules
- Purchase acquisition records with supplier and payment information
- Sales processing that atomically marks inventory as sold
- Dashboard summary with operational metrics, financial totals, and recent activity
- Responsive React interface with loading, error, confirmation, and empty states

## Technology stack

- Backend: Python 3.12, FastAPI, SQLAlchemy, Alembic, PostgreSQL, PyJWT
- Frontend: React, Vite, Material UI, React Router, Axios
- Testing: pytest and FastAPI TestClient

## Architecture

The backend uses versioned REST endpoints under `/api/v1`, Pydantic request/response schemas, JWT dependencies, repositories for database access, and a focused dashboard service for cross-module aggregates. The frontend uses React Router protected routes, a shared authenticated Axios client, page components, and Material UI.

## Project structure

```text
backend/     FastAPI API, Alembic migrations, and tests
frontend/    React/Vite client
docs/        Architecture, design, and testing notes
prompts/     Sprint prompts used during development
```

## Local setup

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 15+

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `DATABASE_URL`, `JWT_SECRET_KEY`, and `CORS_ORIGINS` in `backend/.env`. Generate a strong, unique JWT secret for every deployed environment.

Run migrations and start the API:

```powershell
alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The versioned health endpoint is available at `http://localhost:8000/api/v1/health`, and interactive API documentation is available at `http://localhost:8000/docs`.

### Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` to the deployed API's `/api/v1` URL when deploying. For example: `https://api.example.com/api/v1`.

## Environment variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `APP_NAME` | Yes | FastAPI application title |
| `APP_VERSION` | Yes | API version metadata |
| `ENVIRONMENT` | Yes | Runtime environment label |
| `DATABASE_URL` | Yes | PostgreSQL SQLAlchemy connection URL |
| `JWT_SECRET_KEY` | Yes | Secret used to sign access tokens |
| `JWT_ALGORITHM` | Yes | JWT signing algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Yes | Access-token lifetime |
| `CORS_ORIGINS` | Yes in production | Comma-separated allowed frontend origins |
| `VITE_API_BASE_URL` | Yes in production | Frontend API base URL, including `/api/v1` |

Never commit populated `.env` files or production secrets.

## Authorization

The first user must be created as an `ADMIN`. Afterwards, only administrators can create or manage users.

| Capability | Admin | Employee |
| --- | --- | --- |
| View vehicles, purchases, sales, and dashboard | Yes | Yes |
| Create, edit, or delete vehicles and purchases | Yes | No |
| Manage users | Yes | No |
| Record sales | Yes | Yes, only under their own seller identity |
| Edit or delete sales | Yes | No |

Backend authorization is the enforcement point; frontend route protection prevents unauthenticated access.

## login password for employee:

mail = jack@example.com
password = Password@123
## API overview

| Resource | Base endpoint |
| --- | --- |
| Authentication | `/api/v1/auth/login` |
| Users | `/api/v1/users` |
| Vehicles | `/api/v1/vehicles` |
| Purchases | `/api/v1/purchases` |
| Sales | `/api/v1/sales` |
| Dashboard summary | `/api/v1/dashboard/summary` |
| Dashboard operational metrics | `/api/v1/dashboard/operational-metrics` |
| Dashboard financial metrics | `/api/v1/dashboard/financial-metrics` |
| Dashboard activity | `/api/v1/dashboard/recent-activity` |

Protected endpoints require `Authorization: Bearer <access-token>`.

## Testing and build verification

Run the backend suite:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

Build the frontend production bundle:

```powershell
cd frontend
npm run build
```

The final review executed the backend suite successfully (89 tests passed) and completed the frontend production build successfully.

## Deployment checklist

1. Provision PostgreSQL and configure a production `DATABASE_URL`.
2. Set a strong production `JWT_SECRET_KEY` and explicit `CORS_ORIGINS`.
3. Run `alembic upgrade head`.
4. Deploy the backend with `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT` (adapt the port syntax to the hosting platform if needed).
5. Set `VITE_API_BASE_URL` before building and deploy the frontend `dist/` output with SPA fallback routing enabled.
6. Verify `/api/v1/health`, login, protected API access, and the dashboard after deployment.

## Screenshots

No screenshots are committed to the repository. Capture deployment-specific screenshots after the application is hosted, so they reflect the final environment without exposing data or credentials.

## My AI Usage

OpenAI Codex was used as a development assistant to review repository structure, implement scoped sprint requirements, draft tests, identify configuration/documentation gaps, and run local verification commands. The developer remained responsible for defining requirements, reviewing changes, validating behavior, managing credentials and deployment configuration, and deciding what to commit or deploy. AI assistance improved iteration speed and helped maintain consistency across the backend, frontend, and documentation; it did not replace developer review or accountability.

## License

No license has been selected for this repository.
