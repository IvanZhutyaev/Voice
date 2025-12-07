from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.models.appeal import AppealStatus
from app.schemas.appeal import AppealCreate, AppealUpdate, AppealResponse, AppealListResponse
from app.services.appeal_service import AppealService
from app.services.analytics_service import AnalyticsService
import os
from app.core.config import settings

router = APIRouter()
appeal_service = AppealService()
analytics_service = AnalyticsService()


@router.post("", response_model=AppealResponse, status_code=status.HTTP_201_CREATED)
async def create_appeal(
    appeal_data: AppealCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Создание нового обращения"""
    appeal = await appeal_service.create_appeal(db, appeal_data, current_user.id)
    
    # Логирование события
    await analytics_service.log_event(
        db,
        "appeal_created",
        user_id=current_user.id,
        appeal_id=appeal.id
    )
    
    return appeal


@router.get("", response_model=AppealListResponse)
async def get_appeals(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[AppealStatus] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Получение списка обращений"""
    skip = (page - 1) * size
    
    # Обычные пользователи видят только свои обращения
    user_id = None if current_user.is_admin else current_user.id
    
    appeals, total = await appeal_service.get_appeals(
        db,
        skip=skip,
        limit=size,
        status=status,
        user_id=user_id,
        category=category
    )
    
    pages = (total + size - 1) // size
    
    return {
        "items": appeals,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }


@router.get("/{appeal_id}", response_model=AppealResponse)
async def get_appeal(
    appeal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Получение обращения по ID"""
    appeal = await appeal_service.get_appeal(db, appeal_id)
    
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appeal not found"
        )
    
    # Проверка прав доступа
    if not current_user.is_admin and appeal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return appeal


@router.patch("/{appeal_id}", response_model=AppealResponse)
async def update_appeal(
    appeal_id: int,
    appeal_data: AppealUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновление обращения (только для администраторов)"""
    appeal = await appeal_service.update_appeal(db, appeal_id, appeal_data)
    
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appeal not found"
        )
    
    # Логирование события
    await analytics_service.log_event(
        db,
        "appeal_updated",
        user_id=current_user.id,
        appeal_id=appeal.id,
        metadata={"status": appeal.status.value if appeal.status else None}
    )
    
    return appeal


@router.post("/{appeal_id}/upload", response_model=AppealResponse)
async def upload_image(
    appeal_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Загрузка изображения к обращению"""
    appeal = await appeal_service.get_appeal(db, appeal_id)
    
    if not appeal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appeal not found"
        )
    
    # Проверка прав
    if not current_user.is_admin and appeal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Проверка размера файла
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large"
        )
    
    # Сохранение файла
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = f"{settings.UPLOAD_DIR}/{appeal_id}_{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Обновление списка изображений
    if appeal.images is None:
        appeal.images = []
    appeal.images.append(file_path)
    
    await db.commit()
    await db.refresh(appeal)
    
    return appeal

