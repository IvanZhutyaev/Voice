from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.models.appeal import AppealStatus, AppealCategory, AppealPriority


class AppealBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class AppealCreate(AppealBase):
    category: Optional[AppealCategory] = None
    images: List[str] = []


class AppealUpdate(BaseModel):
    status: Optional[AppealStatus] = None
    priority: Optional[AppealPriority] = None
    department_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None


class AppealResponse(AppealBase):
    id: int
    category: AppealCategory
    status: AppealStatus
    priority: AppealPriority
    district: Optional[str] = None
    images: List[str] = []
    audio: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_sentiment: Optional[str] = None
    ai_confidence: Optional[float] = None
    user_id: int
    department_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AppealListResponse(BaseModel):
    items: List[AppealResponse]
    total: int
    page: int
    size: int
    pages: int

