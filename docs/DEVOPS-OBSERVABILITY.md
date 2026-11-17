# Qalqan DevOps and Observability

## Environments
Development and production are separate deployment targets. Use different hosts, PostgreSQL volumes, credentials and GitHub Environments. Create GitHub Environments named `development` and `production`; configure required reviewers for production. Never share secrets or databases.

## Local development stack
Copy `.env.example` to `.env`, replace the example passwords, then run:

```bash
docker compose -f compose.yaml -f compose.dev.yaml up --build -d
docker compose -f compose.yaml -f compose.dev.yaml ps
```

Open API docs at http://localhost:8000/docs, Grafana at http://localhost:3000, Prometheus at http://localhost:9090 and Alertmanager at http://localhost:9093. Monitoring ports bind to localhost. Grafana credentials come from `GRAFANA_USER` and `GRAFANA_PASSWORD` in `.env`.

Generate synthetic events:

```bash
curl -X POST http://localhost:8000/demo/sos
curl -X POST http://localhost:8000/demo/notification -H 'Content-Type: application/json' -d '{"outcome":"failed"}'
curl -X POST http://localhost:8000/demo/safewalk/start
curl -X POST http://localhost:8000/demo/safewalk/finish
```

These demo endpoints never notify contacts or emergency services and do not access a real user's location.

## OpenTelemetry and application metrics
The FastAPI service exports OTLP metrics, traces and logs to the OpenTelemetry Collector. The Collector exposes metrics for Prometheus, sends traces to Tempo and sends logs to Loki. Grafana provisions Prometheus, Loki and Tempo data sources and the Qalqan application dashboard.

Application metrics:
- `qalqan.sos.activations`: SOS activation attempts.
- `qalqan.sos.transitions`: SOS state transitions.
- `qalqan.notifications.results`: queued, sent, failed and unknown provider outcomes.
- `qalqan.safewalk.active`: current active Safe Walk sessions.

FastAPI instrumentation also records request duration/count and HTTP status dimensions. The Prometheus exporter adds the `qalqan_` namespace prefix to application metric names.

Never add phone numbers, emails, account IDs, precise coordinates, PINs, message bodies or tokens as telemetry attributes or labels. Set retention and access controls before production.

## Alerting and AI on-call
Prometheus evaluates the rules in `observability/alerts.yml`; Alertmanager sends firing and resolved alerts to the AI on-call webhook. The responder retrieves a bounded recent snapshot from Prometheus, Loki and Tempo, then combines it with the relevant runbook. If `OPENAI_API_KEY` is configured, it requests model-backed analysis through an OpenAI-compatible Chat Completions endpoint. Otherwise, it returns deterministic runbook-based analysis. If the model call fails, the safe fallback is used.

The responder is read-only. It has no shell, deployment, restart, database-write, location-access or notification-sending tools. Set `OPENAI_API_KEY`, `OPENAI_BASE_URL` and `OPENAI_MODEL` in the local `.env` or protected environment secrets; never commit keys.

To test the notification alert, post at least three failed synthetic outcomes within five minutes:

```bash
for i in 1 2 3; do
  curl -X POST http://localhost:8000/demo/notification \
    -H 'Content-Type: application/json' -d '{"outcome":"failed"}'
done
```

Allow the Prometheus alert's pending period to elapse, then inspect Alertmanager and the `ai-oncall` container logs. Post successful outcomes afterward and allow the alert to resolve.

## CI/CD and manual promotion
GitHub Actions runs API tests, AI on-call tests, validates local/hosted Compose combinations, and builds both container images. Successful pushes to `main` publish an immutable API image to GHCR tagged with the full commit SHA.

The `Deploy development` workflow is manually triggered with a 40-character image SHA and verifies that the corresponding CI test job succeeded. The `Promote development revision to production` workflow is a separate manual action: it requires a SHA that is an ancestor of `main`, successful CI, the exact confirmation word `PROMOTE`, and approval from the production GitHub Environment.

For each GitHub Environment, configure:
- `DEPLOY_HOST`: host name or IP address.
- `DEPLOY_USER`: SSH deployment user.
- `DEPLOY_SSH_KEY`: private SSH key for that user.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: protected OTLP/HTTP collector endpoint reachable by the app.

The deployment host must have Docker Engine and the Compose plugin, GHCR pull access, and the repository's Compose files at `/opt/qalqan-development` or `/opt/qalqan-production`. The host's GHCR credentials must permit pulling the package. Keep the development and production hosts and secrets separate.

**Infrastructure boundary:** GitHub workflows deploy to already-provisioned hosts; they do not create cloud servers, DNS, TLS certificates, firewall rules or managed databases. Adding GitHub Environment secrets and provisioning the hosts remain owner actions. Do not paste private keys or API tokens into chat or commit them to this repository.

## Rollback
Run the relevant deployment workflow with a previous known-good 40-character image SHA. Keep the corresponding image available in GHCR. Verify `/health`, dashboard metrics and logs after rollback. Reverting an image does not reverse database migrations.

## Verification checklist
- [ ] API and on-call responder tests pass in CI.
- [ ] All Compose combinations validate.
- [ ] API and responder container images build.
- [ ] Development and production use distinct hosts and secrets.
- [ ] Metrics, traces and logs are visible in Grafana.
- [ ] Dashboard displays synthetic application events.
- [ ] Notification alert fires, reaches the responder and resolves.
- [ ] Responder returns model-backed analysis or the deterministic fallback.
- [ ] Production approval and rollback are tested without real user data.
