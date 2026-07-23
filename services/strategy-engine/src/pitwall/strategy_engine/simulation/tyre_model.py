class TyreModel:
    """Deterministic tyre degradation model based on compound."""
    
    # Simple static baseline: ms lost per lap of age
    BASE_DEGRADATION_MS = {
        "SOFT": 150,
        "MEDIUM": 80,
        "HARD": 40,
        "UNKNOWN": 100
    }
    
    @classmethod
    def get_degradation_penalty(cls, compound: str, age_laps: int) -> int:
        base_rate = cls.BASE_DEGRADATION_MS.get(compound, 100)
        # Non-linear drop-off approximation: age * age / 10 * rate
        # For simplicity in this milestone, using linear
        return base_rate * age_laps
