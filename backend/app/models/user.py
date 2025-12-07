from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class UserRole(str, enum.Enum):
    CITIZEN = "citizen"
    OPERATOR = "operator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)  # None для OAuth пользователей
    role = Column(Enum(UserRole), default=UserRole.CITIZEN, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

