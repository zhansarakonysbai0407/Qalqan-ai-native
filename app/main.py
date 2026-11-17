import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "qalqan-api")
resource = Resource.create({"service.name": SERVICE_NAME, "deployment.environment": os.getenv("APP_ENV", "development")})
endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318")

metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics"))
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
meter = metrics.get_meter("qalqan.application")
sos_activations = meter.create_counter("qalqan.sos.activations", description="Number of SOS activation attempts")
sos_transitions = meter.create_counter("qalqan.sos.transitions", description="SOS state transitions")
notification_results = meter.create_counter("qalqan.notifications.results", description="Notification provider outcomes")
safe_walk_active = meter.create_up_down_counter("qalqan.safewalk.active", description="Current active Safe Walk sessions")

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")))
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer("qalqan.application")

logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=f"{endpoint}/v1/logs")))
set_logger_provider(logger_provider)
otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
root_logger = logging.getLogger()
root_logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
root_logger.addHandler(logging.StreamHandler())
root_logger.addHandler(otel_handler)
logger = logging.getLogger("qalqan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Qalqan API starting", extra={"event": "service_start"})
    yield
    logger.info("Qalqan API stopping", extra={"event": "service_stop"})

app = FastAPI(title="Qalqan API", version="1.0.0", lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app)

class NotificationEvent(BaseModel):
    outcome: str = Field(pattern="^(queued|sent|failed|unknown)$")

@app.get("/health")
def health():
    return {"status": "ok", "environment": os.getenv("APP_ENV", "development")}

@app.get("/ready")
def ready():
    return {"status": "ready"}

@app.post("/demo/sos")
def demo_sos():
    with tracer.start_as_current_span("qalqan.demo.sos_activation"):
        sos_activations.add(1, {"result": "accepted"})
        sos_transitions.add(1, {"from_state": "idle", "to_state": "active"})
        logger.info("Demo SOS activation recorded", extra={"event": "sos_activation", "mode": "demo"})
        return {"status": "active", "mode": "demo", "message": "No contacts or emergency services were notified."}

@app.post("/demo/notification")
def demo_notification(event: NotificationEvent):
    notification_results.add(1, {"outcome": event.outcome})
    logger.info("Demo notification outcome recorded", extra={"event": "notification_result", "outcome": event.outcome})
    return {"recorded": event.outcome, "mode": "demo"}

@app.post("/demo/safewalk/start")
def start_safewalk():
    safe_walk_active.add(1)
    logger.info("Demo Safe Walk started", extra={"event": "safewalk_started"})
    return {"status": "active", "mode": "demo"}

@app.post("/demo/safewalk/finish")
def finish_safewalk():
    safe_walk_active.add(-1)
    logger.info("Demo Safe Walk finished", extra={"event": "safewalk_finished"})
    return {"status": "finished", "mode": "demo"}
