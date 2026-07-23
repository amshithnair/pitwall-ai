from pitwall.events.models import PitWallEvent

class TyreProcessor:
    """Stateful processor for tyre wear and stint lengths."""
    def __init__(self):
        self.state = {}
        
    def process_tyre_changed(self, event: PitWallEvent) -> dict:
        stint = getattr(event.payload, "stint_number", 1)
        return {
            "tyre_age_laps": 0,
            "stint_length": 0,
            "estimated_degradation": 0.0
        }
