from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON

Base = declarative_base()

class StrategyRecommendation(Base):
    __tablename__ = "strategy_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    driver_id = Column(String, index=True)
    lap_generated = Column(Integer)
    scenario_name = Column(String)
    total_race_time_ms = Column(Integer)
    estimated_finish_position = Column(Integer)
    risk_score = Column(Float)
    details_json = Column(JSON)
