from django.apps import AppConfig


class AdminLogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.admin_apps.logs"
    label = "admin_logs"
    verbose_name = "System Logs"
