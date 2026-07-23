import pytest
from pitwall.ai_orchestrator.tools.f1_tools import get_strategy_recommendation, get_tyre_prediction, get_race_state

def test_get_strategy_recommendation():
    res = get_strategy_recommendation.run("VER")
    assert "Strategy Recommendation for VER" in res

def test_get_tyre_prediction():
    res = get_tyre_prediction.run("HAM")
    assert "Tyre Prediction for HAM" in res

def test_get_race_state():
    res = get_race_state.run({})
    assert "Current Lap:" in res
