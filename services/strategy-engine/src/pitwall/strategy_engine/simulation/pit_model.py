class PitModel:
    """Calculates deterministic pit time losses."""
    
    BASE_PIT_LOSS_MS = 24000
    SC_PIT_LOSS_MS = 14000
    VSC_PIT_LOSS_MS = 16000
    
    @classmethod
    def calculate_pit_loss(cls, safety_car_active: bool, vsc_active: bool) -> int:
        if safety_car_active:
            return cls.SC_PIT_LOSS_MS
        if vsc_active:
            return cls.VSC_PIT_LOSS_MS
        return cls.BASE_PIT_LOSS_MS
