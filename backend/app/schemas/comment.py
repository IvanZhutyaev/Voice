from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    appeal_id: int
    is_internal: bool = False


class CommentResponse(CommentBase):
    id: int
    appeal_id: int
    user_id: int
    is_internal: bool
    created_at: datetime

    class Config:
        from_attributes = True

