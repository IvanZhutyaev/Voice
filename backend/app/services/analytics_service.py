from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Dict, List
from datetime import datetime, timedelta
from app.models.appeal import Appeal, AppealStatus
from app.models.analytics import AnalyticsEvent


class AnalyticsService:
    """Сервис для аналитики"""
    
    async def get_dashboard_stats(
        self,
        db: AsyncSession,
        days: int = 30
    ) -> Dict:
        """Получение статистики для дашборда"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Общее количество обращений
        total_result = await db.execute(
            select(func.count(Appeal.id))
        )
        total_appeals = total_result.scalar() or 0
        
        # Обращения по статусу
        status_result = await db.execute(
            select(Appeal.status, func.count(Appeal.id))
            .where(Appeal.created_at >= cutoff_date)
            .group_by(Appeal.status)
        )
        appeals_by_status = {status.value: count for status, count in status_result.all()}
        
        # Обращения по категории
        category_result = await db.execute(
            select(Appeal.category, func.count(Appeal.id))
            .where(Appeal.created_at >= cutoff_date)
            .group_by(Appeal.category)
        )
        appeals_by_category = {cat.value: count for cat, count in category_result.all()}
        
        # Обращения по приоритету
        priority_result = await db.execute(
            select(Appeal.priority, func.count(Appeal.id))
            .where(Appeal.created_at >= cutoff_date)
            .group_by(Appeal.priority)
        )
        appeals_by_priority = {pri.value: count for pri, count in priority_result.all()}
        
        # Среднее время решения
        resolved_result = await db.execute(
            select(
                func.avg(
                    func.extract('epoch', Appeal.resolved_at - Appeal.created_at) / 3600
                )
            ).where(
                and_(
                    Appeal.status == AppealStatus.RESOLVED,
                    Appeal.resolved_at.isnot(None)
                )
            )
        )
        avg_resolution_time = resolved_result.scalar() or 0.0
        
        # Процент решенных
        resolved_count_result = await db.execute(
            select(func.count(Appeal.id))
            .where(Appeal.status == AppealStatus.RESOLVED)
        )
        resolved_count = resolved_count_result.scalar() or 0
        resolution_rate = (resolved_count / total_appeals * 100) if total_appeals > 0 else 0.0
        
        # Топ районов
        district_result = await db.execute(
            select(Appeal.district, func.count(Appeal.id))
            .where(
                and_(
                    Appeal.district.isnot(None),
                    Appeal.created_at >= cutoff_date
                )
            )
            .group_by(Appeal.district)
            .order_by(func.count(Appeal.id).desc())
            .limit(10)
        )
        top_districts = [
            {"district": district, "count": count}
            for district, count in district_result.all()
        ]
        
        # Распределение тональности
        sentiment_result = await db.execute(
            select(Appeal.ai_sentiment, func.count(Appeal.id))
            .where(
                and_(
                    Appeal.ai_sentiment.isnot(None),
                    Appeal.created_at >= cutoff_date
                )
            )
            .group_by(Appeal.ai_sentiment)
        )
        sentiment_distribution = {sent: count for sent, count in sentiment_result.all()}
        
        # Timeline обращений
        timeline_result = await db.execute(
            select(
                func.date(Appeal.created_at).label('date'),
                func.count(Appeal.id).label('count')
            )
            .where(Appeal.created_at >= cutoff_date)
            .group_by(func.date(Appeal.created_at))
            .order_by(func.date(Appeal.created_at))
        )
        appeals_timeline = [
            {"date": str(date), "count": count}
            for date, count in timeline_result.all()
        ]
        
        return {
            "total_appeals": total_appeals,
            "appeals_by_status": appeals_by_status,
            "appeals_by_category": appeals_by_category,
            "appeals_by_priority": appeals_by_priority,
            "average_resolution_time": round(avg_resolution_time, 2),
            "resolution_rate": round(resolution_rate, 2),
            "appeals_timeline": appeals_timeline,
            "top_districts": top_districts,
            "sentiment_distribution": sentiment_distribution
        }
    
    async def log_event(
        self,
        db: AsyncSession,
        event_type: str,
        user_id: int = None,
        appeal_id: int = None,
        metadata: Dict = None
    ):
        """Логирование события аналитики"""
        event = AnalyticsEvent(
            event_type=event_type,
            user_id=user_id,
            appeal_id=appeal_id,
            metadata=metadata or {}
        )
        db.add(event)
        await db.commit()

