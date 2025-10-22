"""
Settings for the API keys and more.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    ATC_API_KEY: str
    ATC_BASE_URL: str = "https://api.thucchien.ai"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
