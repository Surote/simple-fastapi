from fastapi import FastAPI
from datetime import datetime
import pytz
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
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
    countries = {code.upper(): name for code, name in pytz.country_names.items()}
    return {
        "message": "Welcome to FastAPI with async!",
        "instructions": "Use the /localtime/{country} endpoint to get the local time.",
        "available_countries": countries
    }

@app.get("/localtime/{country}")
async def get_local_time(country: str):
    try:
        # Get the full name of the country
        country_name = pytz.country_names[country.upper()]
        # Get the timezone(s) for the country (use upper, not lower)
        timezones = pytz.country_timezones.get(country.upper())
        if not timezones:
            return {"error": "No timezone found for this country code"}
        # Get the current local time in the first timezone
        local_time = datetime.now(pytz.timezone(timezones[0]))
        return {
            "country": country_name,
            "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except KeyError:
        return {"error": "Invalid country code or timezone not found"}