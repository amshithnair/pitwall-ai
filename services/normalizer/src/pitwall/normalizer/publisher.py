import logging

import redis
from pitwall.events.redis_broker import RedisEventPublisher
from pitwall.events.validation import EventValidator

logger = logging.getLogger(__name__)


class NormalizedEventPublisher:
    """Publishes validated canonical events."""

    def __init__(self):
        redis_client = redis.Redis(host="redis", port=6379)
        self.publisher = RedisEventPublisher(redis_client=redis_client)

    def publish(self, event, is_live=True):
        try:
            EventValidator.validate(event)
            msg_id = self.publisher.publish(event, is_live=is_live)
            logger.debug(f"Published canonical event {event.event_id} with msg_id {msg_id}")
            return msg_id
        except Exception as e:
            logger.error(f"Failed to publish canonical event: {e}")
