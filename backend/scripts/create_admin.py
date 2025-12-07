import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models.user import User, UserRole
from app.core.security import get_password_hash


async def create_admin():
    """Создание администратора"""
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=False
    )
    
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        from sqlalchemy import select
        
        # Проверка существования админа
        result = await session.execute(
            select(User).where(User.email == "admin@glas.ru")
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Создание админа
        admin = User(
            email="admin@glas.ru",
            full_name="Администратор",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_admin=True,
            is_active=True,
            is_verified=True
        )
        
        session.add(admin)
        await session.commit()
        
        print("Admin user created successfully!")
        print("Email: admin@glas.ru")
        print("Password: admin123")


if __name__ == "__main__":
    asyncio.run(create_admin())

