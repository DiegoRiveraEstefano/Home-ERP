"""Shared infrastructure application configuration."""

from django.apps import AppConfig


class SharedConfig(AppConfig):
    """AppConfig for shared domain components, mixins, and templatetags."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.shared"
    label = "shared"
    verbose_name = "Shared Infrastructure"
