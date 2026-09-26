from django.apps import AppConfig


class FinancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.tenant_apps.finances"
    label = "finances"
    verbose_name = "Domestic Finances"
