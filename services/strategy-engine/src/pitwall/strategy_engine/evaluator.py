from pitwall.strategy_engine.simulation.simulator import StrategySimulator
from pitwall.strategy_engine.database.session import SessionLocal
from pitwall.strategy_engine.database.models import StrategyRecommendation

class StrategyEvaluator:
    """Evaluates candidate strategies and persists the optimal choice."""
    
    def evaluate_scenarios(self, session_id: str, driver_id: str, current_lap: int, total_laps: int = 60):
        # Deterministic static scenarios for milestone 6
        scenarios = [
            {"name": "One Stop (M-H)", "pits": [30], "compounds": ["MEDIUM", "HARD"]},
            {"name": "Two Stop (S-M-M)", "pits": [15, 45], "compounds": ["SOFT", "MEDIUM", "MEDIUM"]}
        ]
        
        results = []
        for s in scenarios:
            res = StrategySimulator.simulate_strategy(current_lap, total_laps, s["pits"], s["compounds"])
            res["scenario_name"] = s["name"]
            res["risk_score"] = len(s["pits"]) * 0.1
            results.append(res)
            
        # Rank by total simulated time (lowest is best)
        results.sort(key=lambda x: x["total_time_ms"])
        best = results[0]
        
        # Persist to database
        with SessionLocal() as db:
            rec = StrategyRecommendation(
                session_id=session_id,
                driver_id=driver_id,
                lap_generated=current_lap,
                scenario_name=best["scenario_name"],
                total_race_time_ms=best["total_time_ms"],
                estimated_finish_position=1,  # simplified
                risk_score=best["risk_score"],
                details_json=best
            )
            db.add(rec)
            db.commit()
            
        return best
