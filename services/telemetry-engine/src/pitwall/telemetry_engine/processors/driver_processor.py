from pitwall.events.models import PitWallEvent

class DriverProcessor:
    """Stateful processor for driver analytics and gaps."""
    def process_position_change(self, event: PitWallEvent) -> dict:
        old_pos = getattr(event.payload, "old_position", 0)
        new_pos = getattr(event.payload, "new_position", 0)
        
        return {
            "gap_to_leader_ms": 0,
            "gap_to_ahead_ms": 0,
            "gap_to_behind_ms": 0,
            "consistency_score": 0.0,
            "average_lap_time_ms": 0,
            "position_changes": abs(old_pos - new_pos)
        }
