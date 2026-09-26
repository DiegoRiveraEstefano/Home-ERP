from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home_erp.apps.common_apps.users"
    label = "users"
    verbose_name = "Users & Identity"
