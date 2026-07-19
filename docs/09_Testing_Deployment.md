# Testing and Deployment Guide

## Verification status

Sprint 20 final verification completed the backend test suite successfully: **89 tests passed**. The frontend production build (`npm run build`) also completed successfully. These checks cover the API's authentication, authorization, vehicle, purchase, sale, user, and dashboard flows, plus production bundle generation.

The following browser-level checks remain deployment-specific and should be completed using the deployed URL: login, a protected page request, a representative vehicle/purchase/sale workflow, and SPA route refresh behaviour.

## Automated verification

### Backend

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

Run the test suite after changes to API behavior, authentication, authorization, database models, or migrations.

### Frontend

```powershell
cd frontend
npm install
npm run build
```

The build output is written to `frontend/dist`. Serve it through a host configured to return the application entry point for unknown client-side routes.

## Production deployment

### 1. Configure the backend

Install dependencies and create the runtime environment from the example file:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set these values in the deployment platform's secret/environment-variable settings rather than committing a populated `.env` file:

| Variable | Production guidance |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection URL for the production database. |
| `JWT_SECRET_KEY` | A unique, long, cryptographically random secret. |
| `CORS_ORIGINS` | Comma-separated, explicit frontend origins, for example `https://app.example.com`. |
| `ENVIRONMENT` | Use `production`. |
| `APP_NAME`, `APP_VERSION`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Set to values appropriate for the release. |

Apply migrations before starting the API:

```powershell
alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Adapt `$PORT` to the hosting platform's startup-command convention. Confirm the service responds at `/health` (and `/api/v1/health`) and that `/docs` is reachable when API documentation is intended to be public.

### 2. Configure and build the frontend

Create `frontend/.env` from `frontend/.env.example` and set the API URL before building:

```text
VITE_API_BASE_URL=https://api.example.com/api/v1
```

Then build and deploy `frontend/dist`:

```powershell
cd frontend
npm install
npm run build
```

The frontend host must support SPA fallback routing so direct navigation to routes such as `/dashboard` or `/vehicles` loads the React application instead of returning a 404 response.

## Release smoke test

After deploying, verify:

- The frontend loads over HTTPS and can reach the configured API.
- `/health` returns `{"status":"ok"}`.
- Login rejects invalid credentials and succeeds for an active account.
- Unauthenticated requests to protected API endpoints return 401.
- Employee accounts cannot perform administrator-only user, vehicle, or purchase mutations.
- A sale is permitted for an employee only when the employee is the seller.
- Dashboard metrics and recent activity load after authentication.
- Refreshing a protected frontend route retains normal SPA routing behavior.

## Deployment limitations

- The repository intentionally does not prescribe a hosting provider, container image, or CI/CD workflow; select these according to the deployment environment.
- Screenshots are not committed. Capture them after deployment with non-sensitive demonstration data if the submission process requires them.
- Backup, monitoring, TLS termination, and database availability are operational responsibilities of the selected hosting platform.
