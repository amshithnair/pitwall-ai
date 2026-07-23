import logging
import redis
from pitwall.events.redis_broker import RedisEventPublisher
from pitwall.events.validation import EventValidator
from pitwall.events.models import PitWallEvent

logger = logging.getLogger(__name__)

class AnalyticsPublisher:
    """Publishes calculated analytics back to the Canonical Event stream."""
    def __init__(self):
        redis_client = redis.Redis(host="redis", port=6379)
        self.publisher = RedisEventPublisher(redis_client=redis_client)
        
    def publish(self, event: PitWallEvent, is_live=False):
        try:
            EventValidator.validate(event)
            msg_id = self.publisher.publish(event, is_live=is_live)
            logger.debug(f"Published Analytics Event {event.event_type} for {event.session_id}")
            return msg_id
        except Exception as e:
            logger.error(f"Failed to publish Analytics Event: {e}")
