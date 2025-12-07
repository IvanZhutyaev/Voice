from app.schemas.user import UserCreate, UserUpdate, UserResponse, Token, LoginRequest
from app.schemas.appeal import (
    AppealCreate,
    AppealUpdate,
    AppealResponse,
    AppealListResponse
)
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.schemas.comment import CommentCreate, CommentResponse
from app.schemas.analytics import AnalyticsResponse

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "Token",
    "LoginRequest",
    "AppealCreate",
    "AppealUpdate",
    "AppealResponse",
    "AppealListResponse",
    "DepartmentCreate",
    "DepartmentResponse",
    "CommentCreate",
    "CommentResponse",
    "AnalyticsResponse"
]

