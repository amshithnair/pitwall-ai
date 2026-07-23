import uuid
from datetime import UTC, datetime
from typing import Generic, TypeVar

from google.protobuf.message import Message
from pitwall.events.proto.envelope_pb2 import EventEnvelope
from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class BasePayload(BaseModel):
    """Base class for all Pydantic event payloads."""

    @classmethod
    def from_proto(cls, proto_msg: Message) -> "BasePayload":
        # Implementation depends on Pydantic and Protobuf conversion
        raise NotImplementedError

    def to_proto(self) -> Message:
        raise NotImplementedError


class PitWallEvent(BaseModel, Generic[T]):
    """Pydantic wrapper for EventEnvelope."""

    schema_version: str = "1.0"
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    session_id: str
    race_id: str
    driver_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sequence: int = 0
    source: str
    payload: T

    def to_protobuf(self) -> EventEnvelope:
        env = EventEnvelope()
        env.schema_version = self.schema_version
        env.event_id = self.event_id
        env.event_type = self.event_type
        env.session_id = self.session_id
        env.race_id = self.race_id
        if self.driver_id:
            env.driver_id = self.driver_id
        env.timestamp.FromDatetime(self.timestamp)
        env.sequence = self.sequence
        env.source = self.source

        # We need to pack the payload into Any
        if hasattr(self.payload, "to_proto"):
            proto_payload = self.payload.to_proto()
            env.payload.Pack(proto_payload)

        return env

    @classmethod
    def from_protobuf(cls, env: EventEnvelope, payload_type: type[T]) -> "PitWallEvent[T]":
        # Unpack the payload
        proto_payload = payload_type.get_proto_class()()
        env.payload.Unpack(proto_payload)

        return cls(
            schema_version=env.schema_version,
            event_id=env.event_id,
            event_type=env.event_type,
            session_id=env.session_id,
            race_id=env.race_id,
            driver_id=env.driver_id if env.HasField("driver_id") else None,
            timestamp=env.timestamp.ToDatetime(),
            sequence=env.sequence,
            source=env.source,
            payload=payload_type.from_proto(proto_payload),
        )
