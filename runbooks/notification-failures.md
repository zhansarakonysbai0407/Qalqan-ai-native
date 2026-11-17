# Notification provider failures

1. Check provider status and credentials without printing secrets.
2. Inspect outcome categories; do not log phone numbers or message bodies.
3. Verify idempotency and retry behavior.
4. Confirm the UI reports failed and unknown states accurately.
5. Use fake providers only; never send test messages to real contacts.
