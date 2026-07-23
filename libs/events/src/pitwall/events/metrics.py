from prometheus_client import Counter, Gauge, Histogram

# Publishing metrics
EVENTS_PUBLISHED = Counter(
    "pitwall_events_published_total", "Total number of events published", ["event_type", "is_live"]
)

PUBLISH_LATENCY = Histogram(
    "pitwall_publish_latency_seconds", "Time taken to publish an event", ["event_type"]
)

# Consumption metrics
EVENTS_CONSUMED = Counter(
    "pitwall_events_consumed_total",
    "Total number of events consumed",
    ["consumer_group", "event_type"],
)

CONSUME_LATENCY = Histogram(
    "pitwall_consume_latency_seconds", "Time taken to process a consumed event", ["consumer_group"]
)

EVENTS_FAILED = Counter(
    "pitwall_events_failed_total",
    "Total number of events that failed processing",
    ["consumer_group", "reason"],
)

STREAM_BACKLOG = Gauge(
    "pitwall_stream_backlog", "Number of pending messages in the consumer group", ["consumer_group"]
)
