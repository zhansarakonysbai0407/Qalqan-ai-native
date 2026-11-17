# API or telemetry unavailable

1. Check container health and the last deployed revision.
2. Inspect application startup logs and OpenTelemetry Collector health.
3. Check database readiness and resource saturation.
4. Compare traces before and after the last release.
5. Escalate to a human before any production restart or rollback.
