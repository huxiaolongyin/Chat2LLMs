from openinference.instrumentation.haystack import HaystackInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

endpoint = "http://localhost:6006/v1/traces"  # The URL to your Phoenix instance
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
HaystackInstrumentor().instrument(tracer_provider=tracer_provider)

from fastapi import FastAPI
from routes import router


def create_app():
    from config import CONFIG

    app = FastAPI(title="Chat2LLM", version=CONFIG.VERSION)

    app.include_router(router, prefix=CONFIG.WEB_ROUTE_PREFIX)

    return app


app = create_app()
