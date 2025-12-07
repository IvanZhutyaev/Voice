import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models.department import Department


async def init_departments():
    """Инициализация департаментов"""
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=False
    )
    
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    departments_data = [
        {
            "name": "Департамент дорожного хозяйства",
            "description": "Ответственен за содержание и ремонт дорог",
            "email": "roads@city.ru",
            "phone": "+79001234567"
        },
        {
            "name": "Департамент благоустройства",
            "description": "Ответственен за благоустройство города",
            "email": "improvement@city.ru",
            "phone": "+79001234568"
        },
        {
            "name": "Департамент экологии",
            "description": "Ответственен за экологию и утилизацию отходов",
            "email": "ecology@city.ru",
            "phone": "+79001234569"
        },
        {
            "name": "Департамент коммунальных услуг",
            "description": "Ответственен за коммунальные услуги",
            "email": "utilities@city.ru",
            "phone": "+79001234570"
        },
        {
            "name": "Департамент безопасности",
            "description": "Ответственен за безопасность в городе",
            "email": "safety@city.ru",
            "phone": "+79001234571"
        }
    ]
    
    async with async_session() as session:
        from sqlalchemy import select
        
        for dept_data in departments_data:
            # Проверка существования
            result = await session.execute(
                select(Department).where(Department.name == dept_data["name"])
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                department = Department(**dept_data)
                session.add(department)
                print(f"Создан департамент: {dept_data['name']}")
            else:
                print(f"Департамент уже существует: {dept_data['name']}")
        
        await session.commit()
        print("Инициализация департаментов завершена!")


if __name__ == "__main__":
    asyncio.run(init_departments())

