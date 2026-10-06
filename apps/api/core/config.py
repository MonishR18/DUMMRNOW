from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List, Union

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6380/0"
    
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    model_config = ConfigDict(env_file=".env")

settings = Settings()
