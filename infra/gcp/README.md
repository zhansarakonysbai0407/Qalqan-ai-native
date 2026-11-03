# Qalqan on Google Cloud Run (Terraform)

This configuration creates an Artifact Registry repository, a Secret Manager secret, and a public Cloud Run service. The service scales down to zero and is capped at two instances.

## Before applying

1. Create/select a Google Cloud project and link a billing account.
2. Enable the Cloud Run, Artifact Registry, Secret Manager, and IAM APIs.
3. Authenticate with an account allowed to create these resources.
4. Copy `terraform.tfvars.example` to `terraform.tfvars` and set the project ID.
5. Build and push the app image to the Artifact Registry repository before creating the Cloud Run service.

The database is **not provisioned by this Terraform configuration**. Use a PostgreSQL provider you have selected and reviewed for pricing. The app needs a PostgreSQL connection URL in Secret Manager.

## Bootstrap before first deployment\n\nThe GitHub Actions deployment workflow has a bootstrap phase. First, run this one-time Terraform bootstrap locally to create the Artifact Registry repository and Secret Manager secret:\n\n```bash\nterraform init\nterraform apply -target=google_project_service.apis -target=google_artifact_registry_repository.qalqan -target=google_secret_manager_secret.database_url\n```\n\nThen add the database connection as the first secret version using the command below. Only after that, trigger the GitHub Actions workflow. The workflow builds and pushes the image, then applies the complete Cloud Run service.\n\nThe workflow supports automatic redeployment on pushes to `main` after you set the repository variable `ENABLE_GCP_DEPLOY=true`. It also supports manual `workflow_dispatch`. Configure these repository secrets: `GCP_PROJECT_ID`, `GCP_WORKLOAD_IDENTITY_PROVIDER`, and `GCP_DEPLOY_SERVICE_ACCOUNT`. Workload Identity Federation must trust this repository and branch.\n\n## Add the database connection secret

After Terraform creates the secret, add its first version from a trusted terminal. Do not commit the URL or put it in `terraform.tfvars`:

```bash
printf '%s' 'postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require' | \
  gcloud secrets versions add qalqan-database-url --data-file=-
```

Use the connection URL supplied by your PostgreSQL provider. Restrict database network access and rotate credentials if they are exposed.

## Apply

```bash
terraform init
terraform plan
terraform apply
```

Terraform creates cloud resources and can incur charges. Review the plan and the current Google Cloud pricing/free-tier conditions before approving `apply`. A zero minimum instance count reduces idle compute use but does not guarantee a zero bill; Artifact Registry, network egress, logs, secret access, and database hosting can still incur costs. Budgets are alerts, not hard spending caps.

## Important MVP limitation

Qalqan currently has a demo SOS flow. Deploying this site does **not** send SOS messages, share live location, or contact emergency services. Do not present the deployed demo as an operational emergency-response service.
