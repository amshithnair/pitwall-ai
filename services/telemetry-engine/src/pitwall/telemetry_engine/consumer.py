import logging
import threading
import time
from pitwall.events.redis_broker import RedisEventSubscriber
from pitwall.events.models import PitWallEvent
from pitwall.telemetry_engine.processors.lap_processor import LapProcessor
from pitwall.telemetry_engine.publisher import AnalyticsPublisher

logger = logging.getLogger(__name__)

class TelemetryConsumer:
    def __init__(self):
        self.subscriber = RedisEventSubscriber(host="redis", port=6379)
        self.publisher = AnalyticsPublisher()
        self.lap_processor = LapProcessor()
        self._running = False
        
    def start(self):
        if not self._running:
            self._running = True
            self.worker_thread = threading.Thread(target=self._consume_loop, daemon=True)
            self.worker_thread.start()
            
    def stop(self):
        self._running = False
        
    def _consume_loop(self):
        logger.info("Starting telemetry consumer loop")
        self.subscriber.subscribe("telemetry_group", "telemetry_worker")
        
        while self._running:
            try:
                events = self.subscriber.consume(batch_size=1000, timeout_ms=1000)
                for event in events:
                    self._process_event(event)
            except Exception as e:
                logger.error(f"Consumer error: {e}")
                time.sleep(1)
                
    def _process_event(self, event: PitWallEvent):
        # Deterministic processing based on event type
        if event.event_type == "telemetry.point":
            self.lap_processor.process_telemetry(event)
            # Would also store to timescale here
        elif event.event_type == "lap.completed":
            lap_analytics = self.lap_processor.process_lap_completed(event)
            # Create a PitWallEvent for LapAnalytics
            from pitwall.events.proto.categories_pb2 import LapAnalytics
            from datetime import datetime, timezone
            
            payload = LapAnalytics(**lap_analytics)
            analytics_event = PitWallEvent(
                event_type="analytics.lap",
                session_id=event.session_id,
                race_id=event.race_id,
                source="telemetry-engine",
                payload=payload,
                timestamp=datetime.now(timezone.utc),
                driver_id=event.driver_id
            )
            self.publisher.publish(analytics_event)
