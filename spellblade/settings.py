"""Django settings for spellblade project."""
from datetime import timedelta
from pathlib import Path
import environ
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

logging.basicConfig(
    filename = BASE_DIR / 'logs/spellblade.log',
    level = logging.ERROR,
    format = '[%(asctime)s][%(levelname)s] %(message)s',
)

logger = logging.getLogger(__name__)

SECRET_KEY = env('SECRET_KEY').strip()
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = list(filter(lambda host: host.strip(), env.list('ALLOWED_HOSTS', default=[])))

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
    'spellblade_core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'spellblade.urls'

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

WSGI_APPLICATION = 'spellblade.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME', default='spellblade').strip(),
        'USER': env('DB_USER', default='spellblade').strip(),
        'PASSWORD': env('DB_PASS').strip(),
        'HOST': env('DB_HOST', default='localhost').strip(),
        'PORT': env.int('DB_PORT', default=5432)
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY_FALLBACKS = list(filter(lambda key: key.strip(), env.list('SECRET_KEY_FALLBACKS', default=[])))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': True,
}

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LANGUAGES = [
    ('en-us', 'English (US)'),
]

CORS_ALLOWED_ORIGINS = list(filter(lambda origin: origin.strip(), env.list('CORS_ALLOWED_ORIGINS', default=[])))

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL').strip()
SERVER_EMAIL = env('SERVER_EMAIL').strip()
ADMINS = [
    (name.strip(), email.strip())
    for admin in env.list('ADMINS', default=[])
    for name, email in [admin.split(':', 1)]
]

EMAIL_HOST = env('EMAIL_HOST').strip()
EMAIL_HOST_USER = env('EMAIL_USER').strip()
EMAIL_HOST_PASSWORD = env('EMAIL_PASS').strip()
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
