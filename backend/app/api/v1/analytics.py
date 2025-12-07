from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()


@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_dashboard(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Получение статистики для дашборда (только для администраторов)"""
    stats = await analytics_service.get_dashboard_stats(db, days=days)
    return stats

