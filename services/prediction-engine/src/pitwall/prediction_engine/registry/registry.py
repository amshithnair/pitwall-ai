from pitwall.prediction_engine.registry.models import RegisteredModel
from pitwall.prediction_engine.registry.session import SessionLocal

class ModelRegistry:
    """API for tracking and loading models."""
    
    @staticmethod
    def register_model(model_name: str, version: str, framework: str, hyperparams: dict, metrics: dict) -> RegisteredModel:
        with SessionLocal() as db:
            model = RegisteredModel(
                model_name=model_name,
                version=version,
                framework=framework,
                hyperparameters=hyperparams,
                metrics_json=metrics,
                status="STAGING"
            )
            db.add(model)
            db.commit()
            db.refresh(model)
            return model
            
    @staticmethod
    def set_production_model(model_name: str, version: str):
        with SessionLocal() as db:
            # Demote current prod
            db.query(RegisteredModel).filter(
                RegisteredModel.model_name == model_name,
                RegisteredModel.status == "PRODUCTION"
            ).update({"status": "ARCHIVED"})
            
            # Promote new
            model = db.query(RegisteredModel).filter(
                RegisteredModel.model_name == model_name,
                RegisteredModel.version == version
            ).first()
            if model:
                model.status = "PRODUCTION"
                db.commit()
