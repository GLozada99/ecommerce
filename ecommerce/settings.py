import os
from pathlib import Path

import dj_database_url

from ecommerce.env_handler import EnvHandler

BASE_DIR = Path(__file__).resolve().parent.parent
handler = EnvHandler()

SECRET_KEY = handler.SECRET_KEY
DEBUG = handler.DEBUG
ALLOWED_HOSTS = handler.ALLOWED_HOSTS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'safedelete',
    'thumbnails',
    'django_extensions',
    'ecommerce.core',
    'ecommerce.products',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
    'default': dj_database_url.config(default=handler.DB_URL)
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
    'st'
]
# Media files
MEDIA_URL = "mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

THUMBNAILS = {
    'METADATA': {
        'BACKEND': 'thumbnails.backends.metadata.DatabaseBackend',
    },
    'STORAGE': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        # You can also use Amazon S3 or any other Django storage backends
    },
    'SIZES': {
        'small': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 100,
                 'height': 100},
                {'PATH': 'thumbnails.processors.crop', 'width': 80,
                 'height': 80}
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
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 240,
                 'height': 240},
                # {'PATH': 'thumbnails.processors.flip',
                #  'direction': 'horizontal'}
            ],
        },
        'large': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 350,
                 'height': 350},
                {'PATH': 'thumbnails.processors.flip',
                 'direction': 'horizontal'}
            ],
        },
        'watermarked': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 20,
                 'height': 20},
                {'PATH': 'thumbnails.processors.add_watermark',
                 'watermark_path': 'watermark.png'}
            ],
        }
    }
}
