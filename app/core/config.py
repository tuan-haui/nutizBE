from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "YouTube Media API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    CORS_ORIGINS: List[str] = ["*"]
    
    REDIS_URL: str = "redis://localhost:6379/0"
    STORAGE_TYPE: str = "local" # local, s3
    S3_BUCKET: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    
    YOUTUBE_COOKIES_BASE64: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
