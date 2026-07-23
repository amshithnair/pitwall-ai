from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DriverState:
    def __init__(self, driver_id: str):
        self.driver_id = driver_id
        self.current_position = 0
        self.gap_to_leader_ms = 0
        self.gap_to_ahead_ms = 0
        self.tyre_compound = "UNKNOWN"
        self.tyre_age_laps = 0
        self.pit_stops = 0

class RaceStateManager:
    """Maintains authoritative race state for strategy simulation."""
    def __init__(self):
        self.session_id: str = ""
        self.current_lap = 1
        self.safety_car_active = False
        self.vsc_active = False
        self.drivers: Dict[str, DriverState] = {}
        
    def get_driver(self, driver_id: str) -> DriverState:
        if driver_id not in self.drivers:
            self.drivers[driver_id] = DriverState(driver_id)
        return self.drivers[driver_id]
        
    def update_from_analytics(self, event_type: str, payload: Any, driver_id: str):
        if not driver_id:
            return
            
        driver = self.get_driver(driver_id)
        
        if event_type == "analytics.lap":
            driver.tyre_age_laps += 1
            lap = getattr(payload, "lap_number", 0)
            if lap > self.current_lap:
                self.current_lap = lap
                
        elif event_type == "analytics.driver":
            driver.gap_to_leader_ms = getattr(payload, "gap_to_leader_ms", driver.gap_to_leader_ms)
            driver.gap_to_ahead_ms = getattr(payload, "gap_to_ahead_ms", driver.gap_to_ahead_ms)
            
        elif event_type == "analytics.tyre":
            driver.tyre_age_laps = getattr(payload, "tyre_age_laps", driver.tyre_age_laps)
            if driver.tyre_age_laps == 0:
                driver.pit_stops += 1

    def update_race_control(self, event_type: str, payload: Any):
        if event_type == "race.control":
            flag = getattr(payload, "flag_type", "GREEN")
            if flag == "SC":
                self.safety_car_active = True
                self.vsc_active = False
            elif flag == "VSC":
                self.vsc_active = True
                self.safety_car_active = False
            elif flag == "GREEN":
                self.safety_car_active = False
                self.vsc_active = False
