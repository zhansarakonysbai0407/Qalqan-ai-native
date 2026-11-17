import asyncio

from fastapi.testclient import TestClient
import responder


client = TestClient(responder.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_alert_uses_safe_runbook_fallback(monkeypatch, tmp_path):
    (tmp_path / "notification-failures.md").write_text(
        "Check provider health and retry queue depth.", encoding="utf-8"
    )
    monkeypatch.setattr(responder, "RUNBOOK_PATH", tmp_path)
    monkeypatch.setattr(
        responder,
        "telemetry_context",
        lambda: asyncio.sleep(0, result='{"targets": "up"}'),
    )
    monkeypatch.setenv("OPENAI_API_KEY", "")

    response = client.post(
        "/alerts",
        json={
            "receiver": "ai-oncall",
            "status": "firing",
            "alerts": [
                {
                    "status": "firing",
                    "labels": {"alertname": "QalqanNotificationFailures", "severity": "warning"},
                    "annotations": {
                        "summary": "Notification failures increased",
                        "runbook": "notification-failures.md",
                    },
                }
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["received"] == 1
    assert body["responses"][0]["mode"] == "rule-based"
    assert "Check provider health" in body["responses"][0]["analysis"]
    assert "targets" in body["responses"][0]["analysis"]
