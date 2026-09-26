# ruff: noqa: E501
"""
With these settings, tests run faster.
"""

from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import TEMPLATES
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ["localhost", "testserver"]

# LANGUAGE
# ------------------------------------------------------------------------------
# Pin the language so translation-dependent assertions are deterministic even
# when compiled ``.mo`` catalogs exist on the developer machine (``*.mo`` is
# gitignored, so a fresh checkout silently falls back to source strings).
LANGUAGE_CODE = "en"

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="uAbAIhnWCUj1vGD4BkTTPLzGcqhc0L3yYpEUNOZzkGHIyY6BXWeUi1jP8v9urT9S",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "http://media.testserver/"

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres:///home_erp",
    ),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)
DATABASES["default"]["CONN_HEALTH_CHECKS"] = env.bool("CONN_HEALTH_CHECKS", default=True)
DATABASES["default"]["OPTIONS"] = {
    "connect_timeout": env.int("DB_CONNECT_TIMEOUT", default=10),
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 10,
    "keepalives_count": 5,
}
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# pyrefly: ignore [bad-typed-dict-key]
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# django-zeal
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["zeal"]
MIDDLEWARE += ["zeal.middleware.zeal_middleware"]
