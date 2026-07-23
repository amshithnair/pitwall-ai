from datetime import UTC, datetime

from pitwall.events.models import PitWallEvent
from pitwall.events.proto.categories_pb2 import SessionStarted, TelemetryPoint


class FastF1Mapper:
    """Maps FastF1 raw data to Canonical Events."""

    @staticmethod
    def map_session_info(raw_data: dict) -> PitWallEvent:
        payload = SessionStarted(
            name=raw_data.get("session_name", "Unknown"),
            type=raw_data.get("session_type", "Unknown"),
            country=raw_data.get("country", "Unknown"),
        )

        session_id = f"{raw_data.get('year')}-{raw_data.get('race')}-{raw_data.get('session')}"
        race_id = f"{raw_data.get('year')}-{raw_data.get('race')}"

        timestamp = (
            datetime.fromisoformat(raw_data["date"]) if raw_data.get("date") else datetime.now(UTC)
        )

        return PitWallEvent(
            event_type="session.started",
            session_id=session_id.lower().replace(" ", "-"),
            race_id=race_id.lower().replace(" ", "-"),
            source="fastf1",
            payload=payload,
            timestamp=timestamp,
        )

    @staticmethod
    def map_telemetry(raw_data: dict) -> PitWallEvent:
        payload = TelemetryPoint(
            speed=float(raw_data.get("Speed") or 0.0),
            rpm=int(raw_data.get("RPM") or 0),
            gear=int(raw_data.get("nGear") or 0),
            throttle=float(raw_data.get("Throttle") or 0.0),
            brake=float(raw_data.get("Brake") or 0.0),
        )

        session_id = f"{raw_data.get('year')}-{raw_data.get('race')}-{raw_data.get('session')}"
        race_id = f"{raw_data.get('year')}-{raw_data.get('race')}"

        return PitWallEvent(
            event_type="telemetry.point",
            session_id=session_id.lower().replace(" ", "-"),
            race_id=race_id.lower().replace(" ", "-"),
            driver_id=str(raw_data.get("Driver", "UNK")),
            source="fastf1",
            payload=payload,
            timestamp=datetime.now(UTC),
        )
