from opentelemetry import metrics
from prometheus_client import start_http_server
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.prometheus_remote_write import (
    PrometheusRemoteWriteMetricsExporter,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter

meter = None
REMOTE_WRITE = "remote_write"
SCRAPE_CONFIG = "scrape_config"
DEFAULT_PICKUP_DURATION = 60
DEFAULT_PROMETHEUS_CLIENT_PORT = 8000
DEFAULT_PROMETHEUS_CLIENT_HOST = "localhost"

def get_meter(config):
    global meter
    if meter is None:
        resource = Resource(attributes={
            SERVICE_NAME: "timeseries_golem"
        })

        exporter_type = config["exporter"]
        exporter = ConsoleMetricExporter()

        if exporter_type == "prometheus":
            mode = config.get("metric_export_mode", REMOTE_WRITE)
            if mode != REMOTE_WRITE:
                scrape_config = config[mode]
                # Start Prometheus client
                start_http_server(port=scrape_config.get("prometheus_client_port", DEFAULT_PROMETHEUS_CLIENT_PORT), addr=scrape_config.get("prometheus_client_host", DEFAULT_PROMETHEUS_CLIENT_HOST))

                # Initialize PrometheusMetricReader which pulls metrics from the SDK
                # on-demand to respond to scrape requests
                reader = PrometheusMetricReader()
            else:
                exporter = PrometheusRemoteWriteMetricsExporter(
                    endpoint=config[mode]["endpoint"],
                )
                reader = PeriodicExportingMetricReader(exporter, config.get("pickup_duration", DEFAULT_PICKUP_DURATION)*1000)
        else:
            reader = PeriodicExportingMetricReader(exporter, config.get("pickup_duration", DEFAULT_PICKUP_DURATION)*1000)


        provider = MeterProvider(resource=resource, metric_readers=[reader])
        metrics.set_meter_provider(provider)
        meter = metrics.get_meter(__name__)

    return meter
   
        
