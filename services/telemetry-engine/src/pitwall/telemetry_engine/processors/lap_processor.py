from typing import Dict
from pitwall.events.models import PitWallEvent

class LapProcessor:
    """Stateful processor for lap analytics."""
    def __init__(self):
        self.state: Dict[str, Dict[str, dict]] = {}
        
    def process_telemetry(self, event: PitWallEvent):
        session_id = event.session_id
        driver = event.driver_id
        
        if session_id not in self.state:
            self.state[session_id] = {}
        if driver not in self.state[session_id]:
            self.state[session_id][driver] = {"max_speed": 0}
            
        speed = getattr(event.payload, "speed_kph", 0)
        if speed > self.state[session_id][driver]["max_speed"]:
            self.state[session_id][driver]["max_speed"] = speed
            
    def process_lap_completed(self, event: PitWallEvent) -> dict:
        session_id = event.session_id
        driver = event.driver_id
        
        lap_time = getattr(event.payload, "lap_time_ms", 0)
        is_pb = getattr(event.payload, "is_personal_best", False)
        
        max_speed = 0
        if session_id in self.state and driver in self.state[session_id]:
            max_speed = self.state[session_id][driver]["max_speed"]
            self.state[session_id][driver]["max_speed"] = 0
            
        return {
            "lap_number": getattr(event.payload, "lap_number", 0),
            "lap_time_ms": lap_time,
            "delta_to_best_ms": 0,
            "is_personal_best": is_pb,
            "is_session_best": False,
            "average_speed_kph": 0,
            "max_speed_kph": max_speed
        }
