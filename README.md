# Qalqan — personal safety app for Kazakhstan

Qalqan is a personal-safety application concept for people in Kazakhstan. The MVP focuses on SOS activation, trusted contacts, consent-based location sharing and a limited Safe Walk check-in flow.

## DevOps and observability
This repository includes a FastAPI telemetry demo, Docker Compose environments, OpenTelemetry Collector, Prometheus, Grafana, Loki, Tempo, Alertmanager and a read-only AI-assisted on-call webhook.

See [DevOps and Observability guide](docs/DEVOPS-OBSERVABILITY.md). Start locally with `cp .env.example .env` and `docker compose -f compose.yaml -f compose.dev.yaml up --build -d`.

**Safety:** demo endpoints generate synthetic events only. They do not send SMS/push messages, access precise location, or contact emergency services.

## Documentation
- [Brainstorm](chat-brainstorm.md)
- [MVP plan](_docs/plan.md)
- [Task backlog](_docs/tasks.md)
- [Process](_docs/process.md)
- [Agent instructions](AGENTS.md)
- [DevOps guide](docs/DEVOPS-OBSERVABILITY.md)
- [Issue #29](https://github.com/zhansarakonysbai0407/Qalqan-ai-native/issues/29)

Configure GitHub Environments named development and production with separate DEPLOY_HOST, DEPLOY_USER and DEPLOY_SSH_KEY secrets. Require reviewer approval for production. No cloud resources or production deployment are created automatically.
