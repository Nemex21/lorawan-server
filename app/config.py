"""
Configuration management for the application
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "sqlite:///./lorawan.db"
    DATABASE_ECHO: bool = False
    
    # Encryption
    AES_KEY: str = "your-32-character-aes-key-here!"
    
    # Gateway
    GATEWAY_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    GATEWAY_HEARTBEAT_INTERVAL: int = 60
    
    # Map
    MAP_CENTER_LAT: float = 0.0
    MAP_CENTER_LON: float = 0.0
    MAP_ZOOM: int = 10
    
    # Message
    MAX_MESSAGE_LENGTH: int = 255
    MESSAGE_TTL: int = 3600
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080"
    ]
    CORS_CREDENTIALS: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/server.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create logs directory if it doesn't exist
log_dir = os.path.dirname(settings.LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)
