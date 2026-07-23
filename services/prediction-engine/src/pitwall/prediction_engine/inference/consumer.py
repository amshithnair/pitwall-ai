import logging
import threading
import time
import numpy as np
import redis
from datetime import datetime, timezone
from pitwall.events.redis_broker import RedisEventSubscriber, RedisEventPublisher
from pitwall.events.models import PitWallEvent
from pitwall.prediction_engine.features.extractor import FeatureExtractor
from pitwall.prediction_engine.inference.server import InferenceServer

logger = logging.getLogger(__name__)

class PredictionConsumer:
    """Consumes analytics events, runs inference, and publishes PredictionEvents."""
    
    def __init__(self):
        redis_client = redis.Redis(host="redis", port=6379)
        self.subscriber = RedisEventSubscriber(redis_client=redis_client)
        self.publisher = RedisEventPublisher(redis_client=redis_client)
        self.inference_server = InferenceServer()
        self._running = False
        
    def start(self):
        if not self._running:
            self._running = True
            self.worker_thread = threading.Thread(target=self._consume_loop, daemon=True)
            self.worker_thread.start()
            
    def stop(self):
        self._running = False
        
    def _consume_loop(self):
        logger.info("Starting prediction consumer loop")
        self.subscriber.subscribe("telemetry_group", "prediction_worker")
        
        while self._running:
            try:
                events = self.subscriber.consume(batch_size=1000, timeout_ms=1000)
                for event in events:
                    self._process_event(event)
            except Exception as e:
                logger.error(f"Prediction Consumer error: {e}")
                time.sleep(1)
                
    def _process_event(self, event: PitWallEvent):
        # Trigger prediction on lap complete
        if event.event_type == "analytics.lap":
            features = FeatureExtractor.extract_tyre_features(event.payload)
            
            # Use inference server
            prediction, meta = self.inference_server.predict("tyre_degradation", features)
            
            if prediction is not None:
                from pitwall.events.proto.categories_pb2 import TyreLifePredicted
                payload = TyreLifePredicted(
                    estimated_laps_remaining=int(prediction),
                    confidence=meta["confidence"],
                    model_version=meta["version"]
                )
                
                prediction_event = PitWallEvent(
                    event_type="prediction.tyre_life",
                    session_id=event.session_id,
                    race_id=event.race_id,
                    source="prediction-engine",
                    payload=payload,
                    timestamp=datetime.now(timezone.utc),
                    driver_id=event.driver_id
                )
                self.publisher.publish(prediction_event)
                logger.debug(f"Published prediction for driver {event.driver_id}: {int(prediction)} laps")
