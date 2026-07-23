import pytest
from pitwall.strategy_engine.simulation.simulator import StrategySimulator
from pitwall.strategy_engine.simulation.pit_model import PitModel
from pitwall.strategy_engine.simulation.tyre_model import TyreModel

def test_simulate_strategy_no_stops():
    res = StrategySimulator.simulate_strategy(1, 10, [], ["MEDIUM"])
    # 10 laps * (85000 + 80*lap)
    assert res["total_time_ms"] > 85000 * 10
    assert res["final_tyre_age"] == 10

def test_simulate_strategy_one_stop():
    res = StrategySimulator.simulate_strategy(1, 10, [5], ["MEDIUM", "HARD"])
    assert res["final_tyre_age"] == 6 # Laps 5, 6, 7, 8, 9, 10
    
def test_pit_loss_sc():
    loss = PitModel.calculate_pit_loss(safety_car_active=True, vsc_active=False)
    assert loss == 14000
    
def test_tyre_penalty():
    loss = TyreModel.get_degradation_penalty("SOFT", 5)
    assert loss == 150 * 5
