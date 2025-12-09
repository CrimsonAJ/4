from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    ADMIN_HOST: str = "0.0.0.0"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    SECRET_KEY: str = "your-secret-key-change-in-production-1234567890"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
