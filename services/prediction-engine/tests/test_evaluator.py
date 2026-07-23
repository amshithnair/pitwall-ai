import numpy as np
from pitwall.prediction_engine.training.evaluator import Evaluator

def test_evaluate_regression():
    y_true = np.array([3, -0.5, 2, 7])
    y_pred = np.array([2.5, 0.0, 2, 8])
    
    metrics = Evaluator.evaluate_regression(y_true, y_pred)
    
    assert "mae" in metrics
    assert "rmse" in metrics
    assert "mse" in metrics
    assert metrics["mae"] > 0
    assert metrics["rmse"] > 0
