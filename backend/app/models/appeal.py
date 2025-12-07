from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class AppealStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    CLOSED = "closed"


class AppealCategory(str, enum.Enum):
    ROADS = "roads"
    LIGHTING = "lighting"
    IMPROVEMENT = "improvement"
    ECOLOGY = "ecology"
    SAFETY = "safety"
    HEALTHCARE = "healthcare"
    UTILITIES = "utilities"
    SOCIAL = "social"
    OTHER = "other"


class AppealPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Appeal(Base):
    __tablename__ = "appeals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(AppealCategory), nullable=False)
    status = Column(Enum(AppealStatus), default=AppealStatus.PENDING, nullable=False)
    priority = Column(Enum(AppealPriority), default=AppealPriority.MEDIUM, nullable=False)
    
    # Геолокация
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    district = Column(String, nullable=True)
    
    # Медиа
    images = Column(JSON, default=list)  # Список путей к изображениям
    audio = Column(String, nullable=True)  # Путь к аудио файлу
    
    # AI анализ
    ai_summary = Column(Text, nullable=True)
    ai_sentiment = Column(String, nullable=True)  # positive, negative, neutral
    ai_confidence = Column(Float, nullable=True)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = Column(Integer, ForeignKey("appeals.id"), nullable=True)
    
    # Связи
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    # Метаданные
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Отношения
    user = relationship("User", backref="appeals")
    department = relationship("Department", backref="appeals")
    comments = relationship("Comment", back_populates="appeal", cascade="all, delete-orphan")

