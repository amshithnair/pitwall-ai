import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from pitwall.prediction_engine.registry.registry import ModelRegistry
from pitwall.prediction_engine.training.evaluator import Evaluator

MODELS_DIR = os.getenv("MODELS_DIR", "./models")

class TrainingPipeline:
    """End-to-end reproducible training pipeline."""
    
    @classmethod
    def train_tyre_model(cls, X_train, y_train, X_val, y_val, version: str):
        # 1. Train Model
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)
        
        # 2. Evaluate
        y_pred = model.predict(X_val)
        metrics = Evaluator.evaluate_regression(y_val, y_pred)
        
        # 3. Serialize
        os.makedirs(MODELS_DIR, exist_ok=True)
        model_path = os.path.join(MODELS_DIR, f"tyre_degradation_v{version}.joblib")
        joblib.dump(model, model_path)
        
        # 4. Register
        hyperparams = {"n_estimators": 50, "random_state": 42}
        ModelRegistry.register_model(
            model_name="tyre_degradation",
            version=version,
            framework="scikit-learn",
            hyperparams=hyperparams,
            metrics=metrics
        )
        
        print(f"Model saved to {model_path} and registered.")
