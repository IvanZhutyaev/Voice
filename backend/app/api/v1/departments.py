from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentResponse
from sqlalchemy import select

router = APIRouter()


@router.get("", response_model=List[DepartmentResponse])
async def get_departments(
    db: AsyncSession = Depends(get_db)
):
    """Получение списка департаментов"""
    result = await db.execute(select(Department).where(Department.is_active.is_(True)))
    departments = result.scalars().all()
    return list(departments)


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_data: DepartmentCreate,
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Создание департамента (только для администраторов)"""
    department = Department(**department_data.model_dump())
    db.add(department)
    await db.commit()
    await db.refresh(department)
    return department


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получение департамента по ID"""
    result = await db.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    return department

