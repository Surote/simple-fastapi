from fastapi import FastAPI, HTTPException
from datetime import datetime
import os
import pytz
import json
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def json_span_formatter(span):
    """Format span as single-line JSON."""
    span_data = {
        "name": span.name,
        "context": {
            "trace_id": format(span.context.trace_id, "032x"),
            "span_id": format(span.context.span_id, "016x"),
        },
        "kind": str(span.kind),
        "parent_id": format(span.parent.span_id, "016x") if span.parent else None,
        "start_time": span.start_time,
        "end_time": span.end_time,
        "status": {
            "status_code": str(span.status.status_code),
        },
        "attributes": dict(span.attributes) if span.attributes else {},
    }
    return json.dumps(span_data, default=str)


provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter(formatter=json_span_formatter))
provider.add_span_processor(processor)

# Set up OTLP exporter to send traces to OTEL Collector (default endpoint: localhost:4317)
otlp_exporter = OTLPSpanExporter()
otlp_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(otlp_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Instrument the app with Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def read_root():
    """
    Root endpoint that provides instructions and a list of available countries.
    """
    countries = {code.upper(): name for code, name in pytz.country_names.items()}
    return {
        "message": "Welcome to FastAPI with async!",
        "instructions": "Use the /localtime/{country} endpoint to get the local time.",
        "available_countries": countries
    }

@app.get("/pod")
async def get_pod_info():
    """Return the pod name this instance is running on."""
    hostname = os.environ.get("HOSTNAME", "unknown")
    return {"pod_name": hostname}

@app.get("/localtime/{country}")
async def get_local_time(country: str):
    """
    Get the current local time for a specific country.
    
    Args:
        country (str): The ISO 3166-1 alpha-2 country code (e.g., US, FR).
        
    Returns:
        dict: Country name, specific timezone used, and local time.
    """
    country_upper = country.upper()
    if country_upper not in pytz.country_names:
        raise HTTPException(status_code=400, detail="Invalid country code")

    timezones = pytz.country_timezones.get(country_upper)
    if not timezones:
        raise HTTPException(status_code=404, detail="No timezone found for this country code")

    selected_timezone = timezones[0]
    local_time = datetime.now(pytz.timezone(selected_timezone))
    return {
        "country": pytz.country_names[country_upper],
        "timezone": selected_timezone,
        "all_timezones": timezones,
        "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S")
    }