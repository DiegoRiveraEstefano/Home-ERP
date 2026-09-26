from django.apps import AppConfig


class AdminMetricsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.admin_apps.metrics"
    label = "admin_metrics"
    verbose_name = "System Metrics"
