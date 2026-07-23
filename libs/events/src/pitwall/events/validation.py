from typing import Any

from pitwall.events.models import PitWallEvent


class EventValidationError(Exception):
    """Raised when an event fails validation."""

    pass


class EventValidator:
    """Runtime validation layer for Canonical Events."""

    @staticmethod
    def validate(event: PitWallEvent[Any]) -> bool:
        if not event.event_type:
            raise EventValidationError("event_type is required")
        if not event.session_id:
            raise EventValidationError("session_id is required")
        if not event.race_id:
            raise EventValidationError("race_id is required")
        if not event.timestamp:
            raise EventValidationError("timestamp is required")
        if not event.source:
            raise EventValidationError("source is required")

        # Ensure schema_version is 1.0
        if event.schema_version != "1.0":
            raise EventValidationError(f"Unsupported schema version: {event.schema_version}")

        return True
