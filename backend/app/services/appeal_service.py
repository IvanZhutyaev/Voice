from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from datetime import datetime
from app.models.appeal import Appeal, AppealStatus
from app.schemas.appeal import AppealCreate, AppealUpdate
from app.ai.classifier import AIClassifier
from app.ai.analyzer import AIAnalyzer
from app.services.geolocation_service import GeolocationService


class AppealService:
    """Сервис для работы с обращениями"""
    
    def __init__(self):
        self.classifier = AIClassifier()
        self.analyzer = AIAnalyzer()
        self.geolocation = GeolocationService()
    
    async def create_appeal(
        self,
        db: AsyncSession,
        appeal_data: AppealCreate,
        user_id: int
    ) -> Appeal:
        """Создание нового обращения"""
        # AI классификация
        ai_result = await self.classifier.classify_appeal(
            appeal_data.title,
            appeal_data.description
        )
        
        # Анализ тональности
        sentiment_result = await self.analyzer.analyze_sentiment(
            f"{appeal_data.title}\n{appeal_data.description}"
        )
        
        # Определение района
        district = None
        if appeal_data.latitude and appeal_data.longitude:
            district = await self.geolocation.get_district(
                appeal_data.latitude,
                appeal_data.longitude
            )
        
        # Получение адреса
        address = appeal_data.address
        if not address and appeal_data.latitude and appeal_data.longitude:
            address = await self.geolocation.get_address_from_coordinates(
                appeal_data.latitude,
                appeal_data.longitude
            )
        
        # Проверка на дубликаты
        existing_appeals = await self._get_recent_appeals(db, user_id)
        duplicate_check = await self.classifier.detect_duplicate(
            f"{appeal_data.title}\n{appeal_data.description}",
            [f"{a.title}\n{a.description}" for a in existing_appeals]
        )
        
        appeal = Appeal(
            title=appeal_data.title,
            description=appeal_data.description,
            category=appeal_data.category or ai_result["category"],
            priority=ai_result["priority"],
            latitude=appeal_data.latitude,
            longitude=appeal_data.longitude,
            address=address,
            district=district,
            images=appeal_data.images,
            user_id=user_id,
            ai_summary=ai_result["summary"],
            ai_sentiment=sentiment_result["sentiment"],
            ai_confidence=ai_result["confidence"],
            is_duplicate=duplicate_check is not None
        )
        
        db.add(appeal)
        await db.commit()
        await db.refresh(appeal)
        
        return appeal
    
    async def get_appeal(
        self,
        db: AsyncSession,
        appeal_id: int
    ) -> Optional[Appeal]:
        """Получение обращения по ID"""
        result = await db.execute(
            select(Appeal).where(Appeal.id == appeal_id)
        )
        return result.scalar_one_or_none()
    
    async def get_appeals(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        status: Optional[AppealStatus] = None,
        user_id: Optional[int] = None,
        category: Optional[str] = None
    ) -> tuple[List[Appeal], int]:
        """Получение списка обращений с пагинацией"""
        query = select(Appeal)
        
        if status:
            query = query.where(Appeal.status == status)
        if user_id:
            query = query.where(Appeal.user_id == user_id)
        if category:
            query = query.where(Appeal.category == category)
        
        # Подсчет общего количества
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Получение данных с пагинацией
        query = query.order_by(Appeal.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        appeals = result.scalars().all()
        
        return list(appeals), total
    
    async def update_appeal(
        self,
        db: AsyncSession,
        appeal_id: int,
        appeal_data: AppealUpdate
    ) -> Optional[Appeal]:
        """Обновление обращения"""
        appeal = await self.get_appeal(db, appeal_id)
        if not appeal:
            return None
        
        update_data = appeal_data.model_dump(exclude_unset=True)
        
        if "status" in update_data:
            appeal.status = update_data["status"]
            if appeal.status == AppealStatus.RESOLVED:
                appeal.resolved_at = datetime.utcnow()
        
        if "priority" in update_data:
            appeal.priority = update_data["priority"]
        if "department_id" in update_data:
            appeal.department_id = update_data["department_id"]
        if "title" in update_data:
            appeal.title = update_data["title"]
        if "description" in update_data:
            appeal.description = update_data["description"]
        
        await db.commit()
        await db.refresh(appeal)
        
        return appeal
    
    async def _get_recent_appeals(
        self,
        db: AsyncSession,
        user_id: int,
        days: int = 30
    ) -> List[Appeal]:
        """Получение недавних обращений пользователя"""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = await db.execute(
            select(Appeal).where(
                and_(
                    Appeal.user_id == user_id,
                    Appeal.created_at >= cutoff_date
                )
            ).limit(10)
        )
        return list(result.scalars().all())

