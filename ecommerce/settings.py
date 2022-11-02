import os
from pathlib import Path

from django.utils.translation import gettext_lazy

from ecommerce.env_settings import Settings

BASE_DIR = Path(__file__).resolve().parent.parent
env_settings = Settings()

SECRET_KEY = env_settings.DJANGO_SECRET_KEY
DEBUG = env_settings.DJANGO_DEBUG
ALLOWED_HOSTS = env_settings.DJANGO_ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = env_settings.DJANGO_CSRF_TRUSTED_ORIGINS
ADMINS = [('Gustavo', 'gu.lozada9@gmail.com')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'safedelete',
    'thumbnails',
    'django_extensions',
    'modeltranslation',
    'django_htmx',

    'ecommerce.core',
    'ecommerce.products',
    'ecommerce.clients',
    'ecommerce.order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'ecommerce.core.context_processors.contact_info_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{env_settings.DB_ENGINE}',
        'NAME': f'{env_settings.DB_NAME}',
        'USER': f'{env_settings.DB_USER}',
        'PASSWORD': f'{env_settings.DB_PASSWORD}',
        'HOST': f'{env_settings.DB_HOST}',
        'PORT': f'{env_settings.get_DB_PORT}',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.NumericPasswordValidator'),
    },
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

LANGUAGES = [
    ('en-us', gettext_lazy('English')),
    ('es', gettext_lazy('Spanish')),
]
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en-us', 'es')

# Static files (CSS, JavaScript, Images)
STATIC_URL = "staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
    'static_dir'
]
COMPRESS_ENABLED = False
# Media files
MEDIA_URL = "mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE = ('django.core.files.storage.FileSystemStorage' if
                        not env_settings.S3_STORAGE else
                        'storages.backends.s3boto3.S3Boto3Storage')

THUMBNAILS = {
    'METADATA': {
        'BACKEND': 'thumbnails.backends.metadata.DatabaseBackend',
    },
    'STORAGE': {
        'BACKEND': DEFAULT_FILE_STORAGE,
    },
    'SIZES': {
        'small': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {
                    'PATH':
                        'thumbnails.processors.resize',
                    'width': 100,
                    'height': 100},
            ],
            'POST_PROCESSORS': [
                {
                    'PATH': 'thumbnails.post_processors.optimize',
                    'png_command': 'optipng -force -o7 "%(filename)s"',
                    'jpg_command': 'jpegoptim -f --strip-all "%(filename)s"',
                },
            ],
        },
        'medium': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 240,
                 'height': 240},
            ],
        },
        'category_frontpage': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 400,
                 'height': 400},
            ],
        },
        'product_list': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 500,
                 'height': 625},
            ],
        },
        'product_detail': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 500,
                 'height': 650},
            ],
        },
        'product_detail_related': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 250,
                 'height': 300},
            ],
        },
        'slide': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 1050,
                 'height': 492},
            ],
        },
        'large': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 490,
                 'height': 700},
            ],
        },
        'watermarked': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize',
                 'width': 20,
                 'height': 20},
                {'PATH': 'thumbnails.processors.add_watermark',
                 'watermark_path': 'watermark.png'}
            ],
        }
    }
}

AUTH_USER_MODEL = 'core.User'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings
SITE_ID = 1
LOGIN_REDIRECT_URL = '/site/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/site/'
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

EMAIL_HOST = env_settings.EMAIL_HOST
EMAIL_USE_TLS = env_settings.EMAIL_USE_TLS
EMAIL_PORT = env_settings.EMAIL_PORT
EMAIL_HOST_USER = env_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env_settings.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = env_settings.EMAIL_HOST_USER

AWS_S3_ACCESS_KEY_ID = env_settings.AWS_S3_ACCESS_KEY_ID
AWS_S3_SECRET_ACCESS_KEY = env_settings.AWS_S3_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = env_settings.AWS_STORAGE_BUCKET_NAME
AWS_QUERYSTRING_AUTH = env_settings.AWS_QUERYSTRING_AUTH
ASW_DEFAULT_ACL = env_settings.ASW_DEFAULT_ACL
