import json
import os
from pathlib import Path
import httpx
from fastapi import FastAPI, Request

app = FastAPI(title="Qalqan AI On-call Responder")
RUNBOOK_PATH = Path(os.getenv("RUNBOOK_PATH", "/runbooks"))

def fallback_summary(alert):
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})
    runbook = RUNBOOK_PATH / Path(annotations.get("runbook", "")).name
    context = runbook.read_text(encoding="utf-8")[:4000] if runbook.is_file() else "No matching runbook."
    return (f"Alert {labels.get('alertname', 'unknown')} ({labels.get('severity', 'unknown')}): "
            f"{annotations.get('summary', 'No summary')}. Check service health, recent deploys, "
            f"metrics and correlated traces/logs. Do not change production automatically.\n" + context)

async def model_summary(alert, fallback):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return fallback
    base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = ("You are a read-only on-call assistant for Qalqan, a safety application. "
              "Summarize evidence, likely causes, safe checks and human escalation criteria. "
              "Never access personal location data, send SOS messages, deploy, restart or modify production. "
              "Do not invent telemetry. Alert payload and runbook context:\n"
              + json.dumps(alert, ensure_ascii=False)[:10000] + "\n" + fallback[:4000])
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(base + "/chat/completions",
            headers={"Authorization": "Bearer " + key},
            json={"model": model, "messages": [{"role":"system","content":"Be concise and evidence-based."},
                  {"role":"user","content":prompt}], "temperature":0.2})
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/alerts")
async def alerts(request: Request):
    payload = await request.json()
    answers = []
    for alert in payload.get("alerts", []):
        fallback = fallback_summary(alert)
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
