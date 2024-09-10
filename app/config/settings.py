from os import getenv
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    # App
    APP_NAME:  str = getenv('APP_NAME', 'FastAPI')
    DEBUG: bool = bool(getenv('DEBUG', False))

    # Database URI
    DATABASE_URI: str = getenv('DATABASE_URI', 'sqlite:///./fastapi.db')

    # App Secret Key
    SECRET_KEY: str = getenv('SECRET_KEY', '4pVjDgvKQW9sAjq8njph2s8cbL6uvH9GT79fe6ui6s6eAuFOalfbyIc5vOkkeMC46UoV0CFzxQvQOVbzGcbemQ')


@lru_cache()
def get_settings() -> Settings:
    return Settings()