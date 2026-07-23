import logging
import os
from typing import Any

import fastf1
import pandas as pd
from pitwall.provider_adapter.base import BaseProvider
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class FastF1Provider(BaseProvider):
    """FastF1 implementation of the provider interface."""

    def __init__(self, cache_dir: str = "/app/fastf1_cache"):
        os.makedirs(cache_dir, exist_ok=True)
        fastf1.Cache.enable_cache(cache_dir)

    def health_check(self) -> bool:
        # FastF1 doesn't have a direct ping, assume healthy if we can import it
        return True

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _load_session(
        self, year: int, race_identifier: str, session_type: str, with_telemetry: bool = False
    ):
        logger.info(f"Loading FastF1 session: {year} {race_identifier} {session_type}")
        session = fastf1.get_session(year, race_identifier, session_type)
        session.load(telemetry=with_telemetry, weather=False)
        return session

    def get_session_info(
        self, year: int, race_identifier: str, session_type: str
    ) -> dict[str, Any]:
        session = fastf1.get_session(year, race_identifier, session_type)
        return {
            "provider": "fastf1",
            "event_name": session.event.EventName,
            "country": session.event.Country,
            "session_name": session.name,
            "date": session.date.isoformat() if session.date else None,
        }

    def get_laps(self, year: int, race_identifier: str, session_type: str) -> list[dict[str, Any]]:
        session = self._load_session(year, race_identifier, session_type, with_telemetry=False)
        df = session.laps

        if df is None or df.empty:
            return []

        # FastF1 uses NaT, replace with None for JSON serialization
        df = df.where(pd.notnull(df), None)

        # Convert timedelta columns to total seconds
        for col in df.select_dtypes(include=["timedelta64[ns]"]).columns:
            df[col] = df[col].dt.total_seconds()

        records = df.to_dict("records")
        return records

    def get_telemetry(
        self, year: int, race_identifier: str, session_type: str
    ) -> list[dict[str, Any]]:
        session = self._load_session(year, race_identifier, session_type, with_telemetry=True)
        car_data = session.car_data

        if not car_data:
            return []

        all_telemetry = []
        for driver, df in car_data.items():
            if df is None or df.empty:
                continue

            df = df.where(pd.notnull(df), None)

            # Convert timedelta columns
            for col in df.select_dtypes(include=["timedelta64[ns]"]).columns:
                df[col] = df[col].dt.total_seconds()

            records = df.to_dict("records")
            for r in records:
                r["Driver"] = driver
            all_telemetry.extend(records)

        return all_telemetry
