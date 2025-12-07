from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from sqlalchemy import select

router = APIRouter()
user_service = UserService()


@router.get("", response_model=List[UserResponse])
async def get_users(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Получение списка пользователей (только для администраторов)"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return list(users)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Получение пользователя по ID (только для администраторов)"""
    user = await user_service.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

