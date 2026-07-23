from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime, timezone

Base = declarative_base()

class RegisteredModel(Base):
    """Tracks metadata for trained ML models."""
    __tablename__ = "registered_models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    version = Column(String, index=True)
    status = Column(String)  # STAGING, PRODUCTION, ARCHIVED
    framework = Column(String) # scikit-learn
    hyperparameters = Column(JSON)
    metrics_json = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
