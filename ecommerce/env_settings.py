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
    DB_PORT_DEV: int
    DB_NAME: str

    AWS_S3_ACCESS_KEY_ID: str
    AWS_S3_SECRET_ACCESS_KEY: str
    AWS_STORAGE_BUCKET_NAME: str
    AWS_QUERYSTRING_AUTH: bool
    ASW_DEFAULT_ACL: str

    EMAIL_HOST: str
    EMAIL_USE_TLS: bool
    EMAIL_PORT: int
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str

    SMALL_THUMBNAIL_NUMBER: int

    class Config:
        case_sensitive = True
        env_file = '.env'

    @property
    def get_DB_PORT(self) -> int:
        return self.DB_PORT_DEV if self.DJANGO_DEBUG else self.DB_PORT
