from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app import main
from app.database import Base
from app import models  # noqa: F401 - registers metadata

client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "qalqan-api"}


def test_readiness_requires_database_tables(monkeypatch):
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)
    monkeypatch.setattr(main, "engine", test_engine)

    response = client.get("/api/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["migrations"] == "applied"
    test_engine.dispose()


def test_readiness_fails_when_schema_is_missing(monkeypatch):
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    monkeypatch.setattr(main, "engine", test_engine)

    response = client.get("/api/ready")

    assert response.status_code == 503
    assert response.json()["detail"]["status"] == "not_ready"
    assert "users" in response.json()["detail"]["missing_tables"]
    test_engine.dispose()
