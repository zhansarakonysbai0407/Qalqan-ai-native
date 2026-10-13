# Qalqan — AI-native workflow

Qalqan is a proposed personal-safety SOS app concept for Kazakhstan. This repository currently contains planning and workflow documentation only; no application code is included yet.

## Current scope decisions
- MVP languages: Kazakh, Russian, English.
- Risk-zone map: deferred to a later version.
- SOS activation: tap and confirm, or press and hold for rapid activation.
- SOS stop: PIN established in advance is required.
- Trusted contacts: up to five.
- Alerts: push and SMS through configured services; delivery must not be claimed until integrations are configured and tested.
- Location: live updates during an active SOS, subject to permissions, connectivity, GPS and OS background limits.
- Safe Walk: **not decided yet**. See `chat-brainstorm.md`.

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

## Status
Documentation and issue-tracking setup only. Requirements are not fully finalized; implementation has intentionally not started.