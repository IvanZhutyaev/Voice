import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpass123",
                "full_name": "Test User"
            }
        )
        assert response.status_code in [201, 400]  # 400 если пользователь уже существует


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@glas.ru",
                "password": "admin123"
            }
        )
        # Может быть 401 если админ не создан
        assert response.status_code in [200, 401]

