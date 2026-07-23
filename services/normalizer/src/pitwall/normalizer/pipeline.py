import json
import logging
import threading
import time

import redis
from pitwall.normalizer.mappers.fastf1_mapper import FastF1Mapper
from pitwall.normalizer.publisher import NormalizedEventPublisher

logger = logging.getLogger(__name__)


class NormalizerPipeline:
    """Consumes raw events and publishes canonical events."""

    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=False)
        self.stream_name = b"pitwall:raw:events"
        self.group_name = b"normalizer_group"
        self.consumer_name = b"normalizer_worker"
        self.publisher = NormalizedEventPublisher()
        self._running = False

        try:
            self.redis.xgroup_create(self.stream_name, self.group_name, id="0", mkstream=True)
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                logger.warning(
                    f"Failed to create consumer group, it might already exist. Exception: {e}"
                )

    def start(self):
        if not self._running:
            self._running = True
            self.worker_thread = threading.Thread(target=self._consume_loop, daemon=True)
            self.worker_thread.start()

    def stop(self):
        self._running = False

    def _consume_loop(self):
        logger.info("Starting normalizer pipeline loop")
        while self._running:
            try:
                results = self.redis.xreadgroup(
                    self.group_name,
                    self.consumer_name,
                    {self.stream_name: b">"},
                    count=100,
                    block=2000,
                )
                if not results:
                    continue

                for _, messages in results:
                    for msg_id, msg_dict in messages:
                        self._process_message(msg_id, msg_dict)
            except redis.exceptions.ConnectionError:
                logger.warning("Redis connection failed, retrying...")
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error in normalizer loop: {e}")
                time.sleep(1)

    def _process_message(self, msg_id: bytes, msg_dict: dict):
        try:
            payload = json.loads(msg_dict[b"payload"].decode("utf-8"))
            provider = payload.get("provider")
            event_type = payload.get("event_type")
            data = payload.get("data")

            # Combine context
            data["year"] = payload.get("year")
            data["race"] = payload.get("race")
            data["session"] = payload.get("session")

            event = None
            if provider == "fastf1":
                if event_type == "session_info":
                    event = FastF1Mapper.map_session_info(data)
                elif event_type == "telemetry":
                    event = FastF1Mapper.map_telemetry(data)

            if event:
                self.publisher.publish(event, is_live=False)

            # Acknowledge
            self.redis.xack(self.stream_name, self.group_name, msg_id)
        except Exception as e:
            logger.error(f"Failed to process raw message {msg_id}: {e}")
