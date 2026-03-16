"""
应用配置
"""

import logging

from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings
from typing import Optional, List

logger = logging.getLogger(__name__)


def _load_env_file() -> None:
    """Load .env with fallback encodings to avoid Unicode errors."""
    env_path = Path(".env")
    if not env_path.exists():
        return
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            load_dotenv(dotenv_path=env_path, encoding=encoding, override=False)
            return
        except UnicodeDecodeError:
            continue
    logger.warning("Failed to decode .env; using process env vars only.")


class Settings(BaseSettings):
    """应用配置类"""

    # 应用配置
    APP_NAME: str = "无限层菜单管理系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = (
        "mysql+pymysql://root:password@localhost:3306/menu_system?charset=utf8mb4"
    )

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    # Redis配置（可选）
    REDIS_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


# Load .env file on module import
_load_env_file()
