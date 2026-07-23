from pitwall.normalizer.mappers.fastf1_mapper import FastF1Mapper


def test_map_session_info():
    raw_data = {
        "session_name": "Race",
        "session_type": "R",
        "country": "UK",
        "year": 2024,
        "race": "silverstone",
        "session": "race",
        "date": "2024-07-07T14:00:00+00:00",
    }

    event = FastF1Mapper.map_session_info(raw_data)
    assert event.event_type == "session.started"
    assert event.session_id == "2024-silverstone-race"
    assert event.race_id == "2024-silverstone"
    assert event.source == "fastf1"


def test_map_telemetry_missing_values():
    raw_data = {
        "year": 2024,
        "race": "monza",
        "session": "fp1",
        "Driver": "VER",
        # Missing Speed, RPM, etc. (None values as mocked by pandas null handling)
        "Speed": None,
        "RPM": None,
    }

    event = FastF1Mapper.map_telemetry(raw_data)
    assert event.event_type == "telemetry.point"
    assert event.driver_id == "VER"
    # Defaults to 0
    assert event.payload.speed == 0.0
    assert event.payload.rpm == 0
