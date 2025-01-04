# pylint: disable=missing-module-docstring
import sys
from datetime import timedelta
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import environ

def venv(key) -> str:
    '''Fetches an environment variable. On failure, exits with an error message.'''
    try:
        return env(key).strip()
    except ImproperlyConfigured:
        sys.exit(f'\033[91m\033[1mImproperlyConfigured: {key} is required but not set.\033[0m')

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = venv('SECRET_KEY')
SECRET_KEY_FALLBACKS = \
    list(filter(lambda key: key.strip(), env.list('SECRET_KEY_FALLBACKS', default=[])))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

if env.bool('DEBUG', default=False):
    DEBUG = True
else:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)

ALLOWED_HOSTS = list(filter(lambda host: host.strip(), env.list('ALLOWED_HOSTS', default=[])))
CORS_ALLOWED_ORIGINS = \
    list(filter(lambda origin: origin.strip(), env.list('CORS_ALLOWED_ORIGINS', default=[])))

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # project-specific apps
    'authapp',
    'coreapp',
]

MIDDLEWARE = [
    # django middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # third-party middlewares
    'corsheaders.middleware.CorsMiddleware',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

ROOT_URLCONF = 'spellblade.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages'
    ]}
}]

WSGI_APPLICATION = 'spellblade.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME', default='spellblade').strip(),
        'USER': env('DB_USER', default='spellblade').strip(),
        'PASSWORD': venv('DB_PASS'),
        'HOST': env('DB_HOST', default='localhost').strip(),
        'PORT': env.int('DB_PORT', default=5432)
    }
}

AUTH_USER_MODEL = 'authapp.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

EMAIL_HOST = venv('EMAIL_HOST')
EMAIL_HOST_USER = venv('EMAIL_USER')
EMAIL_HOST_PASSWORD = venv('EMAIL_PASS')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=f'{EMAIL_HOST_USER}@{EMAIL_HOST}').strip()

SERVER_EMAIL = env('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL).strip()
ADMINS = [
    (name.strip(), email.strip())
    for admin in env.list('ADMINS', default=[])
    for name, email in [admin.split(':')]
]

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
