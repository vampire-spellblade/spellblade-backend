# pylint: disable=missing-module-docstring

from pathlib import Path
from datetime import timedelta
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY').strip()
SECRET_KEY_FALLBACKS = [
    SECRET_KEY_FALLBACK.strip()
        for SECRET_KEY_FALLBACK in env.list('SECRET_KEY_FALLBACKS', default=[])
]
DEBUG = env.bool('DEBUG_VALUE', default=False)

ALLOWED_HOSTS = [
    ALLOWED_HOST.strip()
        for ALLOWED_HOST in env.list('ALLOWED_HOSTS', default=[])
]
CORS_ALLOWED_ORIGINS = [
    CORS_ALLOWED_ORIGIN.strip()
        for CORS_ALLOWED_ORIGIN in env.list('CORS_ALLOWED_ORIGINS', default=[])
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

ROOT_URLCONF = 'spellblade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spellblade.wsgi.application'

SECURE_SSL_REDIRECT = env.bool('SSL_ENABLE', default=True)
SECURE_PROXY_SSL_HEADER = \
    ('HTTP_X_FORWARDED_PROTO', 'https') if env.bool('SSL_ENABLE', default=True) else None
USE_X_FORWARDED_HOST = env.bool('SSL_ENABLE', default=True)
USE_X_FORWARDED_PORT = env.bool('SSL_ENABLE', default=True)

CSRF_COOKIE_SECURE = env.bool('SSL_ENABLE', default=True)
SESSION_COOKIE_SECURE = env.bool('SSL_ENABLE', default=True)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SSL_ENABLE', default=True)
SECURE_HSTS_PRELOAD = env.bool('SSL_ENABLE', default=True)
SECURE_HSTS_SECONDS = int(
    timedelta(days=365).total_seconds()
) if env.bool('SSL_ENABLE', default=True) else 0

DATA_UPLOAD_MAX_NUMBER_FIELDS = 200
DATA_UPLOAD_MAX_NUMBER_FILES = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME', default='spellblade').strip(),
        'USER': env('DB_USER', default='spellblade').strip(),
        'PASSWORD': env('DB_PASSWORD').strip(),
        'HOST': env('DB_HOST', default='localhost').strip(),
        'PORT': env.int('DB_PORT', default=5432),
        'TEST': {'NAME': 'spellblade_test',},
    }
}

AUTH_USER_MODEL = 'account.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'account.validators.PasswordComplexityValidator',},
]

SERVER_EMAIL = env('SERVER_EMAIL').strip()
ADMINS = [
    [(name.strip(), email.strip()) for name, email in [admin.split(':')]].pop()
        for admin in env.list('ADMINS', default=[])
]

EMAIL_HOST = env('EMAIL_HOST').strip()
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', False)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER').strip()
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD').strip()
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL').strip()
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='')

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# TODO: Configure logging
