import pytest
from pitwall.telemetry_engine.processors.driver_processor import DriverProcessor
from pitwall.events.models import PitWallEvent
from pitwall.events.proto.categories_pb2 import PositionChanged
from datetime import datetime, timezone

def test_driver_processor_gaps():
    processor = DriverProcessor()
    
    payload = PositionChanged(old_position=4, new_position=2, overtaken_driver_id="HAM")
    event = PitWallEvent(
        event_type="position.changed",
        session_id="session1",
        race_id="race1",
        driver_id="VER",
        source="fastf1",
        payload=payload,
        timestamp=datetime.now(timezone.utc)
    )
    
    result = processor.process_position_change(event)
    assert result["position_changes"] == 2
