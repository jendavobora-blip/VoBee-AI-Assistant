"""
OpenTelemetry Setup for Vobio AI Studio
Provides distributed tracing and metrics
"""

import os
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

logger = logging.getLogger(__name__)


def setup_telemetry(app=None):
    """Initialize OpenTelemetry with OTLP exporters"""
    
    service_name = os.getenv("OTEL_SERVICE_NAME", "vobio-api")
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    
    # Create resource
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })
    
    try:
        # Setup Tracing
        trace_provider = TracerProvider(resource=resource)
        span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        span_processor = BatchSpanProcessor(span_exporter)
        trace_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(trace_provider)
        
        # Setup Metrics
        metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
        metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=60000)
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
        metrics.set_meter_provider(meter_provider)
        
        # Instrument FastAPI if provided
        if app:
            FastAPIInstrumentor.instrument_app(app)
        
        logger.info(f"OpenTelemetry initialized: {service_name} -> {otlp_endpoint}")
        
        return trace.get_tracer(__name__), metrics.get_meter(__name__)
    
    except Exception as e:
        logger.warning(f"Failed to initialize OpenTelemetry: {e}")
        # Return no-op tracer/meter if OTEL setup fails
        return trace.get_tracer(__name__), metrics.get_meter(__name__)


def get_tracer():
    """Get the global tracer"""
    return trace.get_tracer(__name__)


def get_meter():
    """Get the global meter"""
    return metrics.get_meter(__name__)
