# Qalqan MVP plan

## Problem
A person facing a dangerous situation may need a fast way to alert trusted people and share their location. Qalqan is a proposed safety app, not a replacement for official emergency services.

## Intended users
People in Kazakhstan who want a prepared way to alert trusted contacts during an emergency.

## MVP goals
- Provide two deliberate SOS activation paths.
- Notify up to five trusted contacts using configured push and SMS services.
- Share location updates during an active SOS when device permissions and connectivity permit.
- Require a preconfigured PIN to end an active SOS.
- Support Kazakh, Russian and English.
- Provide a limited Safe Walk timer with manual check-ins.

## Confirmed scope
- Activation: tap + confirmation, or press and hold for quick activation.
- End SOS: PIN required.
- Contacts: maximum five.
- Alerts: push and SMS through configured providers.
- Location: updates during active SOS, subject to device constraints.
- Languages: Kazakh, Russian, English.
- Safe Walk: timer + manual check-ins; no automatic contact escalation in MVP.

## Explicitly deferred / out of scope
- Risk-zone map: deferred to a later version.
- Direct integration with police/emergency dispatch: not assumed and requires separate verification/authorization.
- Automatic Safe Walk escalation to contacts: deferred until false-positive handling and user consent are designed.

## Non-functional and safety requirements
- Clear permission prompts and visible indication while location is shared.
- Handle denied permissions, lost GPS, no network, provider errors, and background restrictions.
- Do not state that an alert was delivered unless delivery is confirmed by the provider.
- Securely store PIN verification data; do not store a plaintext PIN.
- Minimize sensitive data retention and restrict access to location history.
- Provide localized interface and accessible SOS controls.
- Use PostgreSQL as the application database; no SQLite runtime dependency.

## Architecture decision
- Frontend: React + TypeScript, built to static assets.
- Backend: Python + FastAPI, serving API and built frontend assets.
- Database: PostgreSQL.
- Containers: one multi-stage application Dockerfile plus a PostgreSQL service in Docker Compose.
- Browser E2E: Playwright.
- CI/CD: GitHub Actions.
- Infrastructure as code: Google Cloud + Terraform, only after checking budget/free-tier eligibility and obtaining explicit approval for resource creation.

## Release gates
1. Confirm scope and acceptance criteria in GitHub Issues.
2. Review architecture, privacy and safety risks.
3. Implement with tests and code review.
4. Test provider integrations before making delivery claims.
5. Deploy only with documented budget guardrails and user authorization.
