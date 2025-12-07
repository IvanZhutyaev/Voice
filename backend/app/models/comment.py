from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # Внутренний комментарий для операторов
    appeal_id = Column(Integer, ForeignKey("appeals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Отношения
    appeal = relationship("Appeal", back_populates="comments")
    user = relationship("User", backref="comments")

