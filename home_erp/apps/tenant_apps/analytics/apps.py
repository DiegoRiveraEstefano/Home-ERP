from django.apps import AppConfig


class TenantAnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.tenant_apps.analytics"
    label = "tenant_analytics"
    verbose_name = "Household Analytics"
