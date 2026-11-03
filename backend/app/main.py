from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text

from .database import Base, engine
from . import models  # Register SQLAlchemy models before checking the schema.

app = FastAPI(title="Qalqan API", version="0.1.0")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "qalqan-api"}


@app.get("/api/ready")
def readiness():
    required_tables = set(Base.metadata.tables)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            existing_tables = set(inspect(connection).get_table_names())
        missing_tables = sorted(required_tables - existing_tables)
        if missing_tables:
            raise HTTPException(
                status_code=503,
                detail={"status": "not_ready", "missing_tables": missing_tables},
            )
        return {"status": "ready", "database": "connected", "migrations": "applied"}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "not_ready", "database": "unavailable"},
        ) from exc


static_dir = Path(__file__).resolve().parents[1] / "static"
if static_dir.exists():
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    def frontend(full_path: str):
        requested = static_dir / full_path
        if full_path and requested.is_file():
            return FileResponse(requested)
        return FileResponse(static_dir / "index.html")
