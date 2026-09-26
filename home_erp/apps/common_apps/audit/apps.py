from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.common_apps.audit"
    label = "audit"
    verbose_name = "Audit & Activity Logs"
