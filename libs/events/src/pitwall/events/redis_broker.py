import logging
from typing import Any

import redis
from pitwall.events.broker import EventPublisher, EventSubscriber
from pitwall.events.models import PitWallEvent
from pitwall.events.proto.envelope_pb2 import EventEnvelope
from redis.exceptions import ResponseError

logger = logging.getLogger(__name__)


class RedisEventPublisher(EventPublisher):
    """Publishes canonical events to Redis Streams."""

    def __init__(self, redis_client: redis.Redis, stream_prefix: str = "pitwall"):
        self.redis = redis_client
        self.stream_prefix = stream_prefix

    def _get_stream_key(self, is_live: bool, replay_id: str | None = None) -> str:
        if is_live:
            return f"{self.stream_prefix}:live:events"
        if not replay_id:
            raise ValueError("replay_id must be provided if not live")
        return f"{self.stream_prefix}:replay:{replay_id}:events"

    def publish(
        self, event: PitWallEvent[Any], is_live: bool = True, replay_id: str | None = None
    ) -> str:
        stream_key = self._get_stream_key(is_live, replay_id)

        # Override session_id if replayed
        if not is_live and replay_id:
            event.session_id = replay_id

        proto_msg = event.to_protobuf()
        serialized_bytes = proto_msg.SerializeToString()

        message = {b"data": serialized_bytes, b"event_type": event.event_type.encode("utf-8")}

        message_id = self.redis.xadd(stream_key, message, maxlen=1000000, approximate=True)
        return message_id.decode("utf-8")


class RedisEventSubscriber(EventSubscriber):
    """Consumes canonical events from Redis Streams via Consumer Groups."""

    def __init__(
        self, redis_client: redis.Redis, stream_key: str, group_name: str, consumer_name: str
    ):
        self.redis = redis_client
        self.stream_key = stream_key
        self.group_name = group_name
        self.consumer_name = consumer_name

        try:
            self.redis.xgroup_create(self.stream_key, self.group_name, id="0", mkstream=True)
        except ResponseError as e:
            if "BUSYGROUP Consumer Group name already exists" not in str(e):
                raise

    def read_events(self, count: int = 10, block_ms: int = 2000) -> list[tuple[str, EventEnvelope]]:
        streams = {self.stream_key: ">"}
        results = self.redis.xreadgroup(
            self.group_name, self.consumer_name, streams, count=count, block=block_ms
        )

        envelopes = []
        if not results:
            return envelopes

        for stream_name, messages in results:
            for msg_id, message_dict in messages:
                if b"data" in message_dict:
                    env = EventEnvelope()
                    env.ParseFromString(message_dict[b"data"])
                    envelopes.append((msg_id.decode("utf-8"), env))

        return envelopes

    def acknowledge(self, message_id: str) -> None:
        self.redis.xack(self.stream_key, self.group_name, message_id)

    def recover_dead_letters(
        self, min_idle_time_ms: int = 60000
    ) -> list[tuple[str, EventEnvelope]]:
        """Claim messages that have been pending for a long time."""
        pending = self.redis.xpending_ext(self.stream_key, self.group_name, "-", "+", 100)

        to_claim = []
        for msg in pending:
            if msg["time_since_delivered"] > min_idle_time_ms:
                to_claim.append(msg["message_id"])

        if not to_claim:
            return []

        claimed_msgs = self.redis.xclaim(
            self.stream_key, self.group_name, self.consumer_name, min_idle_time_ms, to_claim
        )

        envelopes = []
        for msg_id, message_dict in claimed_msgs:
            if b"data" in message_dict:
                env = EventEnvelope()
                env.ParseFromString(message_dict[b"data"])
                envelopes.append((msg_id.decode("utf-8"), env))

        return envelopes
