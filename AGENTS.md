# Agent instructions

## Project status
MVP requirements are documented in `chat-brainstorm.md` and `_docs/plan.md`. Implement only scoped work tracked by GitHub Issues.

## Workflow
1. Read `chat-brainstorm.md`, `_docs/plan.md`, `_docs/process.md`, and `_docs/tasks.md`.
2. Keep decisions traceable; do not silently alter product scope.
3. Work from a detailed issue with acceptance criteria.
4. Follow the roles in `_docs/team/`: PM defines scope, Engineer implements, QA verifies evidence.
5. Do not mark work done without evidence; do not fabricate issue history, timestamps, tests, integrations, or user approval.
6. Keep documentation and task backlog synchronized.

## Safety requirements
- Never represent demo behavior as a real emergency alert.
- Push/SMS delivery requires configured providers and verified delivery outcomes.
- Location tracking requires explicit permission and must state limitations.
- Do not store plaintext PINs; security design must be reviewed before implementation.
- No automatic Safe Walk escalation in MVP.
- Minimize collection and retention of precise location data.

## Documentation style
Use clear Markdown, decisions, acceptance criteria, risks, and explicit open questions.
