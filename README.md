# Qalqan — personal safety app for Kazakhstan

Qalqan is a personal-safety application concept for people in Kazakhstan. The MVP focuses on SOS activation, trusted contacts, consent-based location sharing and a limited Safe Walk check-in flow.

## MVP decisions
- Languages: Kazakh, Russian and English.
- Risk-zone map: deferred to a later version.
- SOS activation: tap and confirm, or press and hold for rapid activation.
- SOS stop: PIN established in advance is required.
- Trusted contacts: up to five.
- Alerts: push and SMS through configured providers; delivery must not be claimed until integrations are configured and confirmed.
- Location: updates during an active SOS, subject to permissions, connectivity, GPS and OS background limits.
- Safe Walk: included as a limited timer + manual check-in feature. No automatic escalation to contacts in this MVP.

## Planned technical stack
- Frontend: React + TypeScript.
- Backend: Python + FastAPI.
- Database: PostgreSQL.
- Containerization: multi-stage Dockerfile + Docker Compose.
- E2E: Playwright.
- CI: GitHub Actions.
- Cloud IaC: Google Cloud + Terraform, subject to free-tier/credit and budget verification.

## Safety notice
Qalqan is not a replacement for official emergency services. The MVP does not claim direct police/dispatch integration. Real push/SMS delivery requires configured providers and successful delivery confirmation. Location sharing is subject to device permission and platform limitations.

## Documentation
- [Brainstorm history](chat-brainstorm.md)
- [Plan](_docs/plan.md)
- [Task backlog](_docs/tasks.md)
- [Process](_docs/process.md)
- [Task template](_docs/task-template.md)
- [PM role](_docs/team/pm.md)
- [Software Engineer role](_docs/team/software-engineer.md)
- [QA Engineer role](_docs/team/qa-engineer.md)
- [Agent instructions](AGENTS.md)
- [Claude instructions](CLAUDE.md)

## Project status
Requirements and implementation backlog are recorded in GitHub Issues. Application code, tests, provider integrations and deployment must be reported as complete only after implementation and verification. See the [open issues](../../issues).
