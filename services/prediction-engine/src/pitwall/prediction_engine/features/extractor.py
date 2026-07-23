import pandas as pd
from typing import Dict, Any, List

class FeatureExtractor:
    """Extracts deterministic features from Canonical Events for model training and inference."""
    
    COMPOUND_MAP = {"SOFT": 1, "MEDIUM": 2, "HARD": 3, "INTERMEDIATE": 4, "WET": 5, "UNKNOWN": 0}
    
    @classmethod
    def extract_tyre_features(cls, driver_state: Dict[str, Any]) -> pd.DataFrame:
        """Extracts features for tyre degradation and life prediction."""
        
        # In a real system, this would join track temp, fuel load, etc.
        features = {
            "tyre_age_laps": driver_state.get("tyre_age_laps", 0),
            "compound_idx": cls.COMPOUND_MAP.get(driver_state.get("compound", "UNKNOWN"), 0),
            "stint_laps_completed": driver_state.get("stint_laps_completed", 0),
            "gap_to_ahead_ms": driver_state.get("gap_to_ahead_ms", 0),
            "track_temp": driver_state.get("track_temp", 30.0) # mock default for milestone
        }
        
        return pd.DataFrame([features])
        
    @classmethod
    def extract_lap_time_features(cls, driver_state: Dict[str, Any]) -> pd.DataFrame:
        """Extracts features for predicting next lap time."""
        features = {
            "current_lap": driver_state.get("current_lap", 1),
            "fuel_load_kg": 110 - (driver_state.get("current_lap", 1) * 1.5), # Approx burn
            "tyre_age_laps": driver_state.get("tyre_age_laps", 0),
            "compound_idx": cls.COMPOUND_MAP.get(driver_state.get("compound", "UNKNOWN"), 0),
            "traffic_density_ahead": driver_state.get("traffic_density_ahead", 0.0)
        }
        
        return pd.DataFrame([features])
