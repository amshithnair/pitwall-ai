import pytest
from pitwall.prediction_engine.features.extractor import FeatureExtractor

def test_extract_tyre_features():
    driver_state = {
        "tyre_age_laps": 15,
        "compound": "SOFT",
        "stint_laps_completed": 15,
        "gap_to_ahead_ms": 2000
    }
    
    df = FeatureExtractor.extract_tyre_features(driver_state)
    assert len(df) == 1
    assert df.iloc[0]["tyre_age_laps"] == 15
    assert df.iloc[0]["compound_idx"] == 1
    assert df.iloc[0]["stint_laps_completed"] == 15
    assert df.iloc[0]["gap_to_ahead_ms"] == 2000

def test_extract_unknown_compound():
    driver_state = {"compound": "UNKNOWN"}
    df = FeatureExtractor.extract_tyre_features(driver_state)
    assert df.iloc[0]["compound_idx"] == 0
