# Qalqan assignment implementation tracker

This file tracks the current code branch and avoids marking incomplete work as finished.

## Implemented in `assignment/full-stack-implementation`

- [x] React/Vite frontend scaffold with EN/RU/KK language selector.
- [x] FastAPI backend scaffold with health and readiness endpoints.
- [x] PostgreSQL SQLAlchemy models and initial Alembic migration.
- [x] Multi-stage Dockerfile serving frontend and backend in one application container.
- [x] Docker Compose app + PostgreSQL service, health checks and persistent DB volume.
- [x] Frontend unit tests and backend readiness/schema tests.
- [x] Playwright E2E tests for landing page, language switching, SOS demo confirmation/cancel, API health and PostgreSQL/schema readiness.
- [x] GitHub Actions CI jobs for frontend, backend, Compose E2E and Docker build.
- [x] Railway Dockerfile deployment configuration and deployment guide.
- [x] Google Cloud Run Terraform scaffold, Secret Manager integration, and manual GitHub Actions deployment workflow.
- [x] GitHub issues for feature-level E2E follow-up work.

## Not yet complete / requires evidence or user credentials

- [ ] Migrate existing SQLite records. No prior SQLite database was found in the implementation branch; if one exists elsewhere, it must be supplied and migrated with a tested export/import procedure.
- [ ] Implement real authentication, trusted contacts, PIN-protected SOS end flow, Safe Walk and permission-aware location sharing.
- [ ] Implement real SMS/push provider integration and delivery-status handling.
- [ ] Add feature-level E2E tests after those features exist; current tests cover only implemented UI and infrastructure checks.
- [ ] Verify latest GitHub Actions run is green.
- [ ] Deploy the demo to Railway or another selected host and record its URL.
- [ ] Configure a hosted PostgreSQL database and securely add its URL to the hosting platform / Google Secret Manager.
- [ ] Configure Google Cloud Workload Identity Federation secrets and run the manual Terraform deployment.
- [ ] Verify production deployment, migrations and health checks.
- [ ] Configure automatic redeployment on commits after a successful hosted deployment.

## Important

The current SOS button is a demo-only flow. A deployed copy must not be described as sending alerts or contacting emergency services.
