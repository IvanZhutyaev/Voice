from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    phone: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_admin: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

