# ruff: noqa: E501
import re

from .base import *  # noqa: F403
from .base import BASE_DIR
from .base import INSTALLED_APPS
from .base import REDIS_CACHE_URL
from .base import SPECTACULAR_SETTINGS
from .base import TEMPLATES
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["home_erp.cl", "127.0.0.1", "localhost", "127.0.0.1:8000"],
)

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres:///home_erp",
    ),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_HEALTH_CHECKS"] = env.bool("CONN_HEALTH_CHECKS", default=True)
DATABASES["default"]["OPTIONS"] = {
    "connect_timeout": env.int("DB_CONNECT_TIMEOUT", default=10),
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 10,
    "keepalives_count": 5,
    "pool": {
        "min_size": env.int("DB_POOL_MIN_SIZE", default=4),
        "max_size": env.int("DB_POOL_MAX_SIZE", default=32),
        "timeout": env.int("DB_POOL_TIMEOUT", default=10),
        "max_idle": env.int("DB_POOL_MAX_IDLE", default=10),
        "reconnect_timeout": env.int("DB_POOL_RECONNECT_TIMEOUT", default=10),
    },
}
if env.bool("DISABLE_SERVER_SIDE_CURSORS", default=False):
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "KEY_PREFIX": "home_erp_cache",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": env.bool("REDIS_IGNORE_EXCEPTIONS", default=True),
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "CONNECTION_POOL_KWARGS": {
                "max_connections": env.int("REDIS_MAX_CONNECTIONS", default=50),
                "retry_on_timeout": True,
                "health_check_interval": 30,
            },
        },
    },
}

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = env("SESSION_COOKIE_NAME", default="__Secure-sessionid")
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = env("CSRF_COOKIE_NAME", default="__Secure-csrftoken")
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=[
        "https://127.0.0.1",
        "https://127.0.0.1:8000",
        "http://localhost",
        "https://home_erp.cl",
    ],
)
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=60)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=True,
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    default=True,
)
SECURE_REFERRER_POLICY = env(
    "DJANGO_SECURE_REFERRER_POLICY",
    default="strict-origin-when-cross-origin",
)

DISALLOWED_USER_AGENTS = [
    re.compile(pattern)
    for pattern in env.list(
        "DJANGO_DISALLOWED_USER_AGENTS",
        default=[
            r"curl",
            r"wget",
            r"python-requests",
            r"python-urllib",
            r"python-httpx",
            r"sqlmap",
            r"nikto",
            r"nmap",
            r"masscan",
            r"zgrab",
            r"gobuster",
            r"dirbuster",
            r"wpscan",
            r"censys",
        ],
    )
]

# AXES (Brute Force Protection)
# ------------------------------------------------------------------------------
AXES_FAILURE_LIMIT = env.int("AXES_FAILURE_LIMIT", default=5)
AXES_COOLOFF_TIME = env.int("AXES_COOLOFF_TIME", default=1)
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_HANDLER = "axes.handlers.cache.AxesCacheHandler"
AXES_CACHE = "default"
AXES_LOCKOUT_TEMPLATE = "403.html"
AXES_VERBOSE = True

# SESSIONS
# ------------------------------------------------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    ),
]
if "APP_DIRS" in TEMPLATES[0]:
    del TEMPLATES[0]["APP_DIRS"]

# STATIC & MEDIA
# ------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "dbbackup": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": str(BASE_DIR / "backups"),
        },
    },
}
WHITENOISE_MAX_AGE = env.int("WHITENOISE_MAX_AGE", default=31536000)
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="home_erp <noreply@home_erp.cl>",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[home_erp] ",
)
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX
ACCOUNT_EMAIL_VERIFICATION = "optional"

# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# Anymail
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}

# django-compressor
# ------------------------------------------------------------------------------
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
COMPRESS_URL = STATIC_URL  # noqa: F405
COMPRESS_OFFLINE = True

# LOGGING
# ------------------------------------------------------------------------------
LOGS_DIR = BASE_DIR / "logs"
active_handlers = ["console"]
handlers_config = {
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "verbose",
        "level": env("DJANGO_LOG_LEVEL", default="INFO"),
    },
}

try:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    handlers_config["file"] = {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": str(LOGS_DIR / "home_erp.log"),
        "when": "midnight",
        "interval": 1,
        "backupCount": 30,
        "encoding": "utf-8",
        "formatter": "verbose",
        "level": env("DJANGO_LOG_LEVEL", default="INFO"),
    }
    active_handlers.append("file")
except (PermissionError, OSError):
    pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": handlers_config,
    "root": {
        "handlers": active_handlers,
        "level": env("DJANGO_LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django": {
            "handlers": active_handlers,
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "home_erp": {
            "handlers": active_handlers,
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}

# django-rest-framework
SPECTACULAR_SETTINGS["SERVERS"] = [
    {"url": "https://home_erp.cl", "description": "Production server"},
]
