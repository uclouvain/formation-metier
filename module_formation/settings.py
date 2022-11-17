"""
Django settings for module_formation project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%asmyf&@mn$vx1xp8(^hensmbvdd1d*0wy@0l3c@&1pu%30d(0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'dal_queryset_sequence',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'formation_metier.apps.FormationMetierConfig',
    'bootstrap3',
    'schema_graph',
    'django_htmx',
    'django_select2',
    'jquery',
    'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    'celery',
    'dotenv',
    'environ'
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'module_formation.urls'

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

WSGI_APPLICATION = 'module_formation.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-be'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# select2

CACHES = {
    # … default cache config and others
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

OPTIONAL_APPS = ()
OPTIONAL_MIDDLEWARES = ()
OPTIONAL_INTERNAL_IPS = ()
INTERNAL_IPS = (
    '127.0.0.1',)

if os.environ.get("ENABLE_DEBUG_TOOLBAR", "False").lower() == "true":
    OPTIONAL_APPS += ('debug_toolbar',)
    OPTIONAL_MIDDLEWARES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    OPTIONAL_INTERNAL_IPS += ('127.0.0.1',)

# environ.Env.read_env(env_file=os.path.join(BASE_DIR, '../.env'))


import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

INSTALLED_APPS += OPTIONAL_APPS
MIDDLEWARE += OPTIONAL_MIDDLEWARES
INTERNAL_IPS += OPTIONAL_INTERNAL_IPS
API_PERSON_URL = os.environ.get('API_PERSON_URL')
DEFAULT_LOGGER = os.environ.get('DEFAULT_LOGGER')
ROLES_OSIS = os.environ.get('ROLES_OSIS')
