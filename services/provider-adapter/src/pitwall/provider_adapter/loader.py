import json
import logging
from typing import Any

import redis
from pitwall.provider_adapter.registry import ProviderRegistry

logger = logging.getLogger(__name__)


class HistoricalLoader:
    def __init__(self):
        self.registry = ProviderRegistry()
        # Connect to shared Redis instance
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=False)
        self.stream_name = "pitwall:raw:events"

    def load_session(self, provider_name: str, year: int, race_identifier: str, session_type: str):
        logger.info(
            f"Starting historical load: {provider_name} {year} {race_identifier} {session_type}"
        )

        provider = self.registry.get_provider(provider_name)
        if not provider:
            logger.error(f"Provider {provider_name} not found")
            return

        try:
            # 1. Get Session Info
            info = provider.get_session_info(year, race_identifier, session_type)
            self._publish_raw(
                "session_info", info, provider_name, year, race_identifier, session_type
            )

            # 2. Get Laps
            laps = provider.get_laps(year, race_identifier, session_type)
            for lap in laps:
                self._publish_raw("lap", lap, provider_name, year, race_identifier, session_type)

            # 3. Get Telemetry
            telemetry = provider.get_telemetry(year, race_identifier, session_type)
            # Batch publishing would be better, but loop for simplicity
            for point in telemetry:
                self._publish_raw(
                    "telemetry", point, provider_name, year, race_identifier, session_type
                )

            logger.info(f"Historical load complete for {year} {race_identifier} {session_type}")

        except Exception:
            logger.exception("Failed to load historical data")

    def _publish_raw(
        self,
        event_type: str,
        data: dict[str, Any],
        provider: str,
        year: int,
        race: str,
        session: str,
    ):
        payload = {
            "provider": provider,
            "year": year,
            "race": race,
            "session": session,
            "event_type": event_type,
            "data": data,
        }

        message = {b"payload": json.dumps(payload).encode("utf-8")}
        self.redis.xadd(self.stream_name, message, maxlen=1000000, approximate=True)
