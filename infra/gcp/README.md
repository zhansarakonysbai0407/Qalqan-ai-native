# Qalqan on Google Cloud Run (Terraform)

This configuration creates an Artifact Registry repository, a Secret Manager secret, and a public Cloud Run service. The service scales down to zero and is capped at two instances.

## Before applying

1. Create/select a Google Cloud project and link a billing account.
2. Enable the Cloud Run, Artifact Registry, Secret Manager, and IAM APIs.
3. Authenticate with an account allowed to create these resources.
4. Copy `terraform.tfvars.example` to `terraform.tfvars` and set the project ID.
5. Build and push the app image to the Artifact Registry repository before creating the Cloud Run service.

The database is **not provisioned by this Terraform configuration**. Use a PostgreSQL provider you have selected and reviewed for pricing. The app needs a PostgreSQL connection URL in Secret Manager.

## Add the database connection secret

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
