# pylint: disable=missing-module-docstring
from datetime import timedelta
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import environ

def error(message): # pylint: disable=missing-function-docstring
    print(f'\033[91m\033[1mCommandError: {message}\033[0m')

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

try:
    SECRET_KEY = env('SECRET_KEY').strip()
except ImproperlyConfigured:
    error('You must set settings.SECRET_KEY.')

SECRET_KEY_FALLBACKS = \
    list(filter(lambda key: key.strip(), env.list('SECRET_KEY_FALLBACKS', default=())))

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

ALLOWED_HOSTS = list(filter(lambda host: host.strip(), env.list('ALLOWED_HOSTS', default=())))
CORS_ALLOWED_ORIGINS = \
    list(filter(lambda origin: origin.strip(), env.list('CORS_ALLOWED_ORIGINS', default=())))

INSTALLED_APPS = (
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
    'core',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

ROOT_URLCONF = 'spellblade.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': (),
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': (
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages'
    )}
}]

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

AUTH_USER_MODEL = 'account.User'

AUTH_PASSWORD_VALIDATORS = (
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

EMAIL_HOST = env('EMAIL_HOST').strip()
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_USER').strip()
EMAIL_HOST_PASSWORD = env('EMAIL_PASS').strip()
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=f'{EMAIL_HOST_USER}@{EMAIL_HOST}').strip()

SERVER_EMAIL = env('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL).strip()
ADMINS = (
    (name.strip(), email.strip())
    for admin in env.list('ADMINS', default=())
    for name, email in (admin.split(':'))
)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
