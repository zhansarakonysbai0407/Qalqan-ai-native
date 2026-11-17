# Qalqan DevOps and Observability

## Environments
Development and production use separate hosts, PostgreSQL volumes, credentials and GitHub Environments. Configure environments named development and production; require reviewer approval for production. Never share secrets or databases.

## Local stack
Copy .env.example to .env and change local passwords. Run:

```bash
docker compose -f compose.yaml -f compose.dev.yaml up --build -d
```

API docs: http://localhost:8000/docs. Grafana: http://localhost:3000. Prometheus: http://localhost:9090. Alertmanager: http://localhost:9093. Monitoring ports bind to localhost.

Generate synthetic events:

```bash
curl -X POST http://localhost:8000/demo/sos
curl -X POST http://localhost:8000/demo/notification -H 'Content-Type: application/json' -d '{"outcome":"failed"}'
curl -X POST http://localhost:8000/demo/safewalk/start
```

These demo endpoints never notify contacts or emergency services.

## OpenTelemetry and application metrics
FastAPI exports OTLP metrics and traces to the OpenTelemetry Collector. Collector exports metrics for Prometheus, traces to Tempo and logs to Loki. Grafana provisions data sources and a Qalqan dashboard.

Custom metrics: qalqan.sos.activations (activation attempts), qalqan.sos.transitions (state transitions), qalqan.notifications.results (queued/sent/failed/unknown provider outcomes), qalqan.safewalk.active (active Safe Walk sessions). FastAPI instrumentation adds request duration/count and HTTP status dimensions.

Never add phone numbers, emails, account IDs, precise coordinates, PINs, message bodies or tokens as telemetry attributes or labels. Set retention and access controls before production.

## Alerts and AI on-call
Prometheus evaluates alert rules and Alertmanager sends alerts to the AI on-call webhook. If OPENAI_API_KEY is configured, it uses an OpenAI-compatible chat-completions endpoint; otherwise it uses a deterministic runbook-based fallback. The responder is read-only and has no shell, deployment, restart, database-write, location-access or notification-sending tools.

Set OPENAI_API_KEY, OPENAI_BASE_URL and OPENAI_MODEL in the development environment for model-backed analysis. Never commit keys. Trigger the notification alert by posting at least three failed synthetic outcomes within five minutes, then inspect Alertmanager and ai-oncall logs.

## CI/CD and manual promotion
CI tests the API, validates both Compose configurations and builds the application image. Successful pushes to main publish an immutable GHCR image tagged with the commit SHA. Deploy development is manually triggered with an image SHA. Production promotion is a separate manual workflow requiring the exact SHA, the word PROMOTE, a successful CI test check and approval in the production GitHub Environment.

Configure separate environment secrets DEPLOY_HOST, DEPLOY_USER and DEPLOY_SSH_KEY. Hosts must have Docker Compose, GHCR pull access and the repository Compose files at /opt/qalqan-development or /opt/qalqan-production. Creating servers and adding secrets remain owner actions; workflows do not provision cloud resources.

## Rollback
Run the deployment workflow with the previous known-good 40-character image SHA. Keep that image in GHCR. Verify /health, dashboard metrics and logs. Database rollback is separate; reverting an image does not reverse migrations.

## Verification checklist
- [ ] CI tests pass.
- [ ] Compose configs validate.
- [ ] Environments use distinct hosts and secrets.
- [ ] Metrics, traces and logs are visible.
- [ ] Dashboard shows synthetic events.
- [ ] Alert fires and resolves.
- [ ] AI responder returns model-backed or fallback analysis.
- [ ] Production approval and rollback are tested without real user data.
