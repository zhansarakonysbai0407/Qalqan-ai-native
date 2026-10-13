# AI-native development process

## Principle
Use the model to accelerate specification and execution while keeping decisions, ownership, acceptance criteria and verification explicit. This repository is currently in the documentation phase.

## Workflow
1. **Brainstorm:** Ask one focused question at a time; capture choices in `chat-brainstorm.md`.
2. **Plan (PM):** Convert confirmed decisions into scope, constraints, risks and open questions in `plan.md`.
3. **Backlog (PM):** Create small, reviewable tasks in `tasks.md` and GitHub Issues.
4. **Engineer:** For an approved issue, propose the smallest change that meets its acceptance criteria. Do not begin implementation while requirements are open.
5. **QA:** Verify each acceptance criterion and record evidence. Use PASS/FAIL/BLOCKED; do not claim tests ran unless they actually ran.
6. **Close:** Close an issue only when its defined completion conditions are met. Record blockers honestly.
7. **Learn:** Update plan/backlog/process when decisions or evidence change.

## Issue lifecycle
- **Open:** scope and acceptance criteria are clear enough to work on.
- **In progress:** work is being performed.
- **Review:** implementation/documentation is ready for independent verification.
- **Closed:** all required acceptance criteria have evidence and QA is complete, or the issue is explicitly closed as not planned with a reason.

GitHub does not have native “in progress” status in the basic issue state; use labels or comments if configured. Never manipulate dates or claim a task was completed before it was.

## Required issue structure
- Context/problem
- Goal and out-of-scope
- Deliverables
- Acceptance criteria (checkboxes)
- QA checklist and evidence
- Dependencies/blockers
- Definition of done

## Safety-critical features
For location and SOS flows, verify permission denial, offline behavior, provider failure, stale location, cancellation/termination, localization and user feedback before any release.