from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.sql import func
from app.core.database import Base


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)  # appeal_created, appeal_resolved, etc.
    user_id = Column(Integer, nullable=True)
    appeal_id = Column(Integer, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

