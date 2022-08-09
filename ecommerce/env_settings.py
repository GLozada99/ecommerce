from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Class to handle environment variables and other constants."""
    DJANGO_SECRET_KEY: str
    DJANGO_DEBUG: bool = False
    DJANGO_ALLOWED_HOSTS: list = Field(default=['localhost'])

    DB_ENGINE: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        case_sensitive = True
        env_file = '.env'
