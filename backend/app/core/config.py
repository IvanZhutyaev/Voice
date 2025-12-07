from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://glas_user:glas_password@postgres:5432/glas_db"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 604800  # 7 days in seconds
    
    # Security
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    ALLOWED_HOSTS: List[str] = ["*"]
    ENVIRONMENT: str = "development"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # Maps
    MAP_API_KEY: str = ""
    
    # File uploads
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # AI Settings
    AI_MODEL: str = "gpt-3.5-turbo"
    AI_TEMPERATURE: float = 0.3
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

