from django.apps import AppConfig


class AdminAnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.admin_apps.analytics"
    label = "admin_analytics"
    verbose_name = "Platform Analytics"
