# Qalqan — personal safety app prototype

Qalqan is a personal-safety application concept for Kazakhstan. This repository now contains a full-stack starter for the assignment: React/Vite frontend, FastAPI backend, PostgreSQL schema/migrations, Docker Compose, Playwright E2E tests, and GitHub Actions CI.

## Current implementation status

- **Frontend:** responsive demo UI with English, Russian, and Kazakh language selection.
- **SOS:** confirmation dialog and demo-only result. No real alerts are sent.
- **Backend:** FastAPI health/readiness endpoints; readiness checks PostgreSQL connectivity and required schema tables.
- **Database:** PostgreSQL via SQLAlchemy and Alembic initial migration. No legacy SQLite data migration has been performed because no existing SQLite application/data store was identified in this branch.
- **Docker:** one multi-stage Dockerfile builds the frontend and serves it from FastAPI; Compose starts the app and PostgreSQL.
- **Tests:** frontend unit tests, backend health/readiness tests, and Playwright tests for landing page, language switching, SOS demo flow, API and PostgreSQL readiness.
- **CI:** frontend, backend, Docker build and Compose-backed E2E workflow.
- **Deployment:** Railway configuration and Google Cloud Run Terraform/workflow scaffolding are included. Hosted deployment is not complete until external accounts, secrets, database URL and a successful deploy are configured.

## Run locally

```bash
cp .env.example .env
# Change the local PostgreSQL password in .env before sharing or deploying.
docker compose up --build
```

Open http://localhost:8000. API health: http://localhost:8000/api/health. Database readiness: http://localhost:8000/api/ready.

Run frontend tests:

```bash
cd frontend
npm install
npm test
npm run build
```

Run backend tests:

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

Run Playwright E2E from the repository root after starting the Compose stack:

```bash
npm install
npx playwright install chromium
npx playwright test
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) and [Google Cloud Terraform instructions](infra/gcp/README.md). Cloud resources are not created automatically. Review provider pricing and configure secrets before deploying.

## Safety notice

This is a software prototype, not an operational emergency-response service. There is no user authentication, trusted-contact CRUD API, PIN verification, SMS/push integration, live location pipeline, Safe Walk backend, or police/emergency-services integration. Do not rely on this demo in a real emergency.
