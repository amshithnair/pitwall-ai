import pytest
from pitwall.telemetry_engine.processors.lap_processor import LapProcessor
from pitwall.events.models import PitWallEvent
from pitwall.events.proto.categories_pb2 import TelemetryPoint, LapCompleted
from datetime import datetime, timezone

def test_lap_processor_tracks_max_speed():
    processor = LapProcessor()
    
    telemetry_payload = TelemetryPoint(speed_kph=300)
    event1 = PitWallEvent(
        event_type="telemetry.point",
        session_id="session1",
        race_id="race1",
        driver_id="VER",
        source="fastf1",
        payload=telemetry_payload,
        timestamp=datetime.now(timezone.utc)
    )
    processor.process_telemetry(event1)
    
    lap_payload = LapCompleted(lap_number=1, lap_time_ms=85000, is_personal_best=True)
    event2 = PitWallEvent(
        event_type="lap.completed",
        session_id="session1",
        race_id="race1",
        driver_id="VER",
        source="fastf1",
        payload=lap_payload,
        timestamp=datetime.now(timezone.utc)
    )
    
    result = processor.process_lap_completed(event2)
    assert result["lap_number"] == 1
    assert result["lap_time_ms"] == 85000
    assert result["max_speed_kph"] == 300
    assert result["is_personal_best"] is True
