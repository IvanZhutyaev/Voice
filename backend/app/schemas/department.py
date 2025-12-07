from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

