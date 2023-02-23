from os import path, mkdir
from os.path import join, exists
from pathlib import Path

from .config_data import (
    KEY
)

BASE_DIR = Path(__file__).resolve().parent.parent
GENERAL_DIR = BASE_DIR.parent
DB_DIR = GENERAL_DIR / 'db'

SECRET_KEY = KEY

DEBUG = True

ALLOWED_HOSTS = []

DJANGO_DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DOWNLOADED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders'
]

PROJECT_APPS = [
    'project.apps.authorization',
]

INSTALLED_APPS = DJANGO_DEFAULT_APPS + DOWNLOADED_APPS + PROJECT_APPS

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]

AUTH_USER_MODEL = 'authorization.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.network.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = join(GENERAL_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = join(GENERAL_DIR, 'media')

NAME_BASE_STATIC_DIRS = '/developer_static/'

FOLDERS_FOR_CREATE = ['db', "developer_static"]

STATICFILES_DIRS = (
    join(GENERAL_DIR, f"{GENERAL_DIR}{NAME_BASE_STATIC_DIRS}"),
)

for folder in FOLDERS_FOR_CREATE:
    if not exists(f'{GENERAL_DIR}/{folder}'):
        mkdir(f'{GENERAL_DIR}/{folder}')

LANGUAGE_CODE = 'UK'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
