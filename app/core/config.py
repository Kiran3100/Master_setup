from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # Pydantic v2 configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='allow'  # Allow extra fields from .env
    )
    
    # Application
    APP_NAME: str = "Levitica HR Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database - PostgreSQL Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "levitica_hr"
    
    # Database URL (auto-generated from above or can be set directly)
    DATABASE_URL: Optional[str] = None
    
    # Connection Pool Settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 minutes
    DB_ECHO: bool = False  # Set to True for SQL query logging
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # File Upload
    MAX_FILE_SIZE: int = 4 * 1024 * 1024  # 4MB
    UPLOAD_DIR: str = "uploads/profile_images"
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg", "image/gif"]
    
    # Superadmin
    SUPERADMIN_EMAIL: str = "superadmin@levitica.com"
    SUPERADMIN_PASSWORD: str = "Admin@123"
    SUPERADMIN_NAME: str = "Super Administrator"
    
    @property
    def database_url(self) -> str:
        """Generate PostgreSQL database URL with proper password encoding"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # URL-encode the password to handle special characters
        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()