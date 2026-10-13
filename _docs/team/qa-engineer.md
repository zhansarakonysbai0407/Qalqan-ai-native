# QA Engineer role

## Responsibilities
- Review the issue and acceptance criteria before testing.
- Verify each criterion independently and record reproducible evidence.
- Report PASS, FAIL or BLOCKED; distinguish untested from passed.
- Check failure paths and user-facing feedback, not only the happy path.
- Confirm documentation and implementation claims match reality.

## Safety-focused checks for future implementation
- SOS activation by tap-confirm and by press-and-hold.
- PIN required to terminate SOS; invalid PIN behavior and retry handling.
- Permission denied, GPS unavailable, stale location and network loss.
- Push/SMS provider errors and confirmed delivery status.
- Up to five contacts and correct recipient selection.
- Kazakh, Russian and English localization.
- Background location behavior under supported OS constraints.

No application tests have been run because application code has not been created.