from typing import List, Dict
from pitwall.strategy_engine.simulation.tyre_model import TyreModel
from pitwall.strategy_engine.simulation.pit_model import PitModel
from pitwall.strategy_engine.simulation.traffic_model import TrafficModel

class StrategySimulator:
    """Deterministically simulates a race strategy from current lap to end."""
    
    BASE_LAP_MS = 85000  # Base lap time: 1:25.000
    
    @classmethod
    def simulate_strategy(cls, current_lap: int, total_laps: int, pit_laps: List[int], compound_choices: List[str]) -> Dict:
        total_time_ms = 0
        current_compound_idx = 0
        tyre_age = 0
        
        if not compound_choices:
            compound_choices = ["UNKNOWN"]
            
        for lap in range(current_lap, total_laps + 1):
            if lap in pit_laps:
                total_time_ms += PitModel.calculate_pit_loss(False, False)
                current_compound_idx = min(current_compound_idx + 1, len(compound_choices) - 1)
                tyre_age = 0
                
            tyre_age += 1
            compound = compound_choices[current_compound_idx]
            deg_penalty = TyreModel.get_degradation_penalty(compound, tyre_age)
            total_time_ms += cls.BASE_LAP_MS + deg_penalty
            
        return {
            "total_time_ms": total_time_ms,
            "final_tyre_age": tyre_age
        }
