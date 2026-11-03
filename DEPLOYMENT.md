# Deployment guide

## Local Docker Compose

```bash
cp .env.example .env
# Change POSTGRES_PASSWORD and DATABASE_URL in .env.
docker compose up --build
```

Open http://localhost:8000. The app and API are served from one container; PostgreSQL runs as a separate Compose service with a persistent volume.

## Railway (first hosted demo)

The repository includes `railway.toml` and a single multi-stage `Dockerfile`. Create a Railway project from this GitHub repository, add a PostgreSQL service, and configure the app service to use the Dockerfile. Set `DATABASE_URL` to the Railway PostgreSQL connection string in the app service variables. Railway's GitHub integration can deploy new commits after the service is configured.

The local Docker Compose file remains the reproducible development/test stack. A managed hosting platform may represent the database as a separate managed service rather than deploying the Compose file as-is. Check current plan pricing and usage limits before deploying.

## Google Cloud production-style deployment\n\nThe GitHub Actions workflow can be manually triggered. To enable automatic deployments from `main`, configure the three `GCP_*` repository secrets and set the repository variable `ENABLE_GCP_DEPLOY` to `true`. Follow the bootstrap and Secret Manager instructions in [infra/gcp/README.md](infra/gcp/README.md).

See [infra/gcp/README.md](infra/gcp/README.md). The Terraform configuration and manual GitHub Actions workflow are scaffolding; they do not create cloud resources until you configure Google Cloud identity and run the workflow. You must also add a PostgreSQL URL to Secret Manager. Review costs before applying.

## Safety disclaimer

The current SOS interaction is a frontend demo only. There is no authentication, contact-management API, SMS/push provider, live location pipeline, or emergency-service integration. A public deployment is a software demonstration, not a working emergency response system.
