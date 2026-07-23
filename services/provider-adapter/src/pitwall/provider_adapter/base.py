from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    """Abstract interface for all data providers."""

    @abstractmethod
    def health_check(self) -> bool:
        """Check if provider is reachable."""
        pass

    @abstractmethod
    def get_session_info(
        self, year: int, race_identifier: str, session_type: str
    ) -> dict[str, Any]:
        """Get high-level session metadata."""
        pass

    @abstractmethod
    def get_laps(self, year: int, race_identifier: str, session_type: str) -> list[dict[str, Any]]:
        """Get lap timing data."""
        pass

    @abstractmethod
    def get_telemetry(
        self, year: int, race_identifier: str, session_type: str
    ) -> list[dict[str, Any]]:
        """Get raw high-frequency telemetry."""
        pass
