import json
import os
import time
from pathlib import Path
import httpx
from fastapi import FastAPI, Request

app = FastAPI(title="Qalqan AI On-call Responder")
RUNBOOK_PATH = Path(os.getenv("RUNBOOK_PATH", "/runbooks"))

async def telemetry_context():
    """Fetch a small, bounded snapshot; never query or expose personal user data."""
    context = {}
    now = int(time.time())
    async with httpx.AsyncClient(timeout=5) as client:
        requests = {
            "prometheus_targets": (os.getenv("PROMETHEUS_URL", "http://prometheus:9090") + "/api/v1/query",
                                  {"query": "up"}),
            "recent_application_logs": (os.getenv("LOKI_URL", "http://loki:3100") + "/loki/api/v1/query_range",
                                        {"query": '{service_name="qalqan-api"}', "limit": "10",
                                         "direction": "BACKWARD", "start": str((now-300)*1000000000),
                                         "end": str(now*1000000000)}),
            "recent_traces": (os.getenv("TEMPO_URL", "http://tempo:3200") + "/api/search",
                              {"limit": "5", "start": str(now-300), "end": str(now)})
        }
        for name, (url, params) in requests.items():
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                context[name] = response.json()
            except Exception as exc:
                context[name] = {"unavailable": type(exc).__name__}
    return json.dumps(context, ensure_ascii=False)[:10000]

def fallback_summary(alert, telemetry="Telemetry context not available."):
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})
    runbook = RUNBOOK_PATH / Path(annotations.get("runbook", "")).name
    runbook_text = runbook.read_text(encoding="utf-8")[:4000] if runbook.is_file() else "No matching runbook."
    return (f"Alert {labels.get('alertname', 'unknown')} ({labels.get('severity', 'unknown')}): "
            f"{annotations.get('summary', 'No summary')}. Check service health, recent deploys, "
            f"metrics and correlated traces/logs. Do not change production automatically.\n"
            f"Runbook:\n{runbook_text}\nTelemetry snapshot:\n{telemetry}")

async def model_summary(alert, fallback):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return fallback
    base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = ("You are a read-only on-call assistant for Qalqan, a safety application. "
              "Analyze the alert, bounded telemetry snapshot and runbook. Separate observed evidence "
              "from hypotheses; give likely causes, safe diagnostic checks and human escalation criteria. "
              "Never access personal location data, send SOS messages, deploy, restart or modify production. "
              "Do not invent telemetry.\n\n" + json.dumps(alert, ensure_ascii=False)[:10000]
              + "\n\nRunbook and telemetry context:\n" + fallback[:10000])
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(base + "/chat/completions",
            headers={"Authorization": "Bearer " + key},
            json={"model": model, "messages": [{"role":"system","content":"Be concise, evidence-based and safety-first."},
                  {"role":"user","content":prompt}], "temperature":0.2})
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/alerts")
async def alerts(request: Request):
    payload = await request.json()
    context = await telemetry_context()
    answers = []
    for alert in payload.get("alerts", []):
        fallback = fallback_summary(alert, context)
        try:
            analysis = await model_summary(alert, fallback)
            mode = "model" if os.getenv("OPENAI_API_KEY") else "rule-based"
        except Exception as exc:
            analysis = fallback + f"\nModel unavailable ({type(exc).__name__}); safe fallback used."
            mode = "fallback"
        item = {"alert": alert.get("labels", {}).get("alertname", "unknown"),
                "status": alert.get("status"), "mode": mode, "analysis": analysis}
        print(json.dumps(item, ensure_ascii=False), flush=True)
        answers.append(item)
    return {"received":len(answers), "responses":answers}
