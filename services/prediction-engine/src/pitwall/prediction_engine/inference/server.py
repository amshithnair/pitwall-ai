import os
import joblib
import logging
from pitwall.prediction_engine.registry.models import RegisteredModel
from pitwall.prediction_engine.registry.session import SessionLocal

logger = logging.getLogger(__name__)
MODELS_DIR = os.getenv("MODELS_DIR", "./models")

class InferenceServer:
    """Manages loaded models and executes fast inference."""
    
    def __init__(self):
        self.models = {}
        
    def load_production_model(self, model_name: str):
        with SessionLocal() as db:
            prod_model = db.query(RegisteredModel).filter(
                RegisteredModel.model_name == model_name,
                RegisteredModel.status == "PRODUCTION"
            ).first()
            
            if not prod_model:
                logger.warning(f"No PRODUCTION model found for {model_name}. Looking for STAGING...")
                prod_model = db.query(RegisteredModel).filter(
                    RegisteredModel.model_name == model_name,
                    RegisteredModel.status == "STAGING"
                ).order_by(RegisteredModel.created_at.desc()).first()
                
            if not prod_model:
                logger.error(f"No model available for {model_name}.")
                return False
                
            model_path = os.path.join(MODELS_DIR, f"{model_name}_v{prod_model.version}.joblib")
            if os.path.exists(model_path):
                self.models[model_name] = {
                    "model": joblib.load(model_path),
                    "version": prod_model.version
                }
                logger.info(f"Loaded {model_name} version {prod_model.version}")
                return True
            else:
                logger.error(f"Model file not found at {model_path}")
                return False
                
    def predict(self, model_name: str, features: object) -> tuple:
        if model_name not in self.models:
            success = self.load_production_model(model_name)
            if not success:
                return None, None
                
        # Scikit-learn inference
        model_wrapper = self.models[model_name]
        prediction = model_wrapper["model"].predict(features)
        
        # Simple deterministic confidence for milestone (inverse of variance from trees)
        confidence = 0.85
        if hasattr(model_wrapper["model"], "estimators_"):
            preds = [est.predict(features) for est in model_wrapper["model"].estimators_]
            variance = np.var(preds, axis=0)[0]
            confidence = max(0.1, min(0.99, 1.0 - (variance / 100.0)))
            
        return prediction[0], {
            "confidence": float(confidence),
            "version": model_wrapper["version"]
        }
