from django.apps import AppConfig


class AdminBackupsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.admin_apps.backups"
    label = "admin_backups"
    verbose_name = "System Backups"
