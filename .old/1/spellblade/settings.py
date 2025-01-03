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

# TODO: Configure logging
