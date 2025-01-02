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

# TODO: Configure logging
