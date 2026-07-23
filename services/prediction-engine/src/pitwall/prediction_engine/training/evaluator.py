from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

class Evaluator:
    """Calculates deterministic metrics for regression and classification models."""
    
    @staticmethod
    def evaluate_regression(y_true, y_pred) -> dict:
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        
        return {
            "mae": mae,
            "rmse": rmse,
            "mse": mse
        }
