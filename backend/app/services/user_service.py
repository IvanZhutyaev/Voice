from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.core.security import create_access_token
from datetime import timedelta


class UserService:
    """Сервис для работы с пользователями"""
    
    async def create_user(
        self,
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        """Создание нового пользователя"""
        # Проверка существования пользователя
        existing_user = await self.get_user_by_email(db, user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        hashed_password = get_password_hash(user_data.password)
        
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            hashed_password=hashed_password
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
    
    async def get_user_by_email(
        self,
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        """Получение пользователя по email"""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(
        self,
        db: AsyncSession,
        user_id: int
    ) -> Optional[User]:
        """Получение пользователя по ID"""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def authenticate_user(
        self,
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """Аутентификация пользователя"""
        user = await self.get_user_by_email(db, email)
        if not user:
            return None
        
        if not user.hashed_password:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    async def create_access_token_for_user(self, user: User) -> str:
        """Создание JWT токена для пользователя"""
        return create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(seconds=604800)  # 7 days
        )

