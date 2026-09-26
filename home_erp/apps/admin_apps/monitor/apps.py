from django.apps import AppConfig


class AdminMonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.admin_apps.monitor"
    label = "admin_monitor"
    verbose_name = "System Monitor"
