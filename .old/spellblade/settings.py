SECRET_KEY_FALLBACKS = list(filter(lambda key: key.strip(), env.list('SECRET_KEY_FALLBACKS', default=[])))

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

if not env.bool('DEBUG', default=False):
    SECURE_SSL_REDIRECT = True

    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
]

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

AUTH_USER_MODEL = 'spellblade_auth.User'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

EMAIL_HOST = env('EMAIL_HOST').strip()
EMAIL_HOST_USER = env('EMAIL_USER').strip()
EMAIL_HOST_PASSWORD = env('EMAIL_PASS').strip()
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
