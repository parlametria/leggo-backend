"""
Django settings for agorapi project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'segredo secreto')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') not in ['False', 'false', 'FALSE']

# LEGGO CSV SERVER variables
CSVS_SERVER_URL = os.getenv('CSVS_SERVER_URL', 'localhost')
CSVS_SERVER_USER = os.getenv('CSVS_SERVER_USER', 'user')
CSVS_SERVER_PWD = os.getenv('CSVS_SERVER_PWD', 'pwd')
CSVS_STORAGE_DIR = os.getenv('CSVS_STORAGE_DIR', './data/')

ALLOWED_HOSTS = [
    'web', '0.0.0.0', 'localhost', '127.0.0.1', '150.165.85.25', 'api',
    'agorapi', 'httpapi', '*'
]

ON_HEROKU = os.environ.get('ON_HEROKU')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'api'
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'agorapi.urls'

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

WSGI_APPLICATION = 'agorapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', ''),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT',  5432)
    }
}

if ON_HEROKU:
    DATABASES['default'] = dj_database_url.config()
    # Redirect HTTP requests to HTTPS
    SECURE_SSL_REDIRECT = True
else:
    SECURE_SSL_REDIRECT = False

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Paths
PROJECT_APP_PATH = Path(__file__).resolve().parent
PROJECT_APP = str(PROJECT_APP_PATH.stem)
PROJECT_ROOT = BASE_DIR = PROJECT_APP_PATH.parent

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = PROJECT_ROOT / STATIC_URL.strip("/")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = ['127.0.0.1']

if DEBUG:
    # tricks to have debug toolbar when developing with docker
    MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.insert(0, 'debug_toolbar')
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']
