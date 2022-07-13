from decouple import UndefinedValueError, config, Csv


class EnvHandler:
    """Class to handle environment variables."""

    # Django settings
    SECRET_KEY = config('DJANGO_SECRET_KEY')
    DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS',
                           default='127.0.0.1', cast=Csv())

    def __init__(self):
        try:
            db_name = config('DB_NAME')
            db_user = config('DB_USER')
            db_pass = config('DB_PASSWORD')
            db_host = config('DB_HOST')
            db_port = config('DB_PORT')
            self.DB_URL = (
                f'postgresql://'
                f'{db_user}:'
                f'{db_pass}@'
                f'{db_host}:'
                f'{db_port}/'
                f'{db_name}'
            )
        except UndefinedValueError:
            self.DB_URL = config('DATABASE_URL')
