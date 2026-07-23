import logging
from collections.abc import Iterator
from typing import Any

from pitwall.events.models import PitWallEvent

logger = logging.getLogger(__name__)


class EventStore:
    """Interface for retrieving historical events for replay."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_event_iterator(
        self, session_id: str, chunk_size: int = 1000
    ) -> Iterator[PitWallEvent[Any]]:
        """
        Yields canonical events for a session, ordered by timestamp.
        Fetches events in chunks from TimescaleDB to manage memory.
        """
        # TODO: Implement actual TimescaleDB chunked querying.
        logger.warning(
            f"EventStore is a stub. Would fetch events for {session_id} from {self.connection_string}"
        )
        yield from []
