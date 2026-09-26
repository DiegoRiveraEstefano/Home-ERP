from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.tenant_apps.inventory"
    label = "inventory"
    verbose_name = "Inventory & Pantry"
