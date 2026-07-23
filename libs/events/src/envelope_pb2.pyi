import datetime
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class EventEnvelope(_message.Message):
    __slots__ = (
        "schema_version",
        "event_id",
        "event_type",
        "session_id",
        "race_id",
        "driver_id",
        "timestamp",
        "sequence",
        "source",
        "payload",
    )
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    RACE_ID_FIELD_NUMBER: _ClassVar[int]
    DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    schema_version: str
    event_id: str
    event_type: str
    session_id: str
    race_id: str
    driver_id: str
    timestamp: _timestamp_pb2.Timestamp
    sequence: int
    source: str
    payload: _any_pb2.Any
    def __init__(
        self,
        schema_version: str | None = ...,
        event_id: str | None = ...,
        event_type: str | None = ...,
        session_id: str | None = ...,
        race_id: str | None = ...,
        driver_id: str | None = ...,
        timestamp: datetime.datetime | _timestamp_pb2.Timestamp | _Mapping | None = ...,
        sequence: int | None = ...,
        source: str | None = ...,
        payload: _any_pb2.Any | _Mapping | None = ...,
    ) -> None: ...
