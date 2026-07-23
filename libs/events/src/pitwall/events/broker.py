from abc import ABC, abstractmethod
from typing import Any

from pitwall.events.models import PitWallEvent
from pitwall.events.proto.envelope_pb2 import EventEnvelope


class EventPublisher(ABC):
    """Abstract base class for publishing Canonical Events."""

    @abstractmethod
    def publish(
        self, event: PitWallEvent[Any], is_live: bool = True, replay_id: str | None = None
    ) -> str:
        """
        Publish an event to the message broker.

        Args:
            event: The PitWallEvent to publish.
            is_live: True if this is a live event, False if it's a replayed event.
            replay_id: Required if is_live is False, used to isolate replay streams.

        Returns:
            The message ID assigned by the broker.
        """
        pass


class EventSubscriber(ABC):
    """Abstract base class for consuming Canonical Events."""

    @abstractmethod
    def read_events(self, count: int = 10, block_ms: int = 2000) -> list[tuple[str, EventEnvelope]]:
        """
        Read pending events from the stream.

        Args:
            count: Maximum number of events to return.
            block_ms: Milliseconds to block waiting for events.

        Returns:
            A list of tuples containing (message_id, event_envelope).
        """
        pass

    @abstractmethod
    def acknowledge(self, message_id: str) -> None:
        """
        Acknowledge a processed message to remove it from the consumer's pending list.

        Args:
            message_id: The ID of the message to acknowledge.
        """
        pass

    @abstractmethod
    def recover_dead_letters(
        self, min_idle_time_ms: int = 60000
    ) -> list[tuple[str, EventEnvelope]]:
        """
        Attempt to claim messages that have been pending for longer than min_idle_time_ms.

        Args:
            min_idle_time_ms: Minimum time in ms a message must be pending before being claimed.

        Returns:
            A list of recovered tuples containing (message_id, event_envelope).
        """
        pass
