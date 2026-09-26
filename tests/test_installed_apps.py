from django.apps import apps
from django.conf import settings


def test_domestic_apps_installed():
    """Verify that all domestic domain apps are installed in INSTALLED_APPS."""
    expected_apps = [
        "home_erp.apps.common_apps.users",
        "home_erp.apps.tenant_apps.households",
        "home_erp.apps.tenant_apps.finances",
        "home_erp.apps.tenant_apps.inventory",
        "home_erp.apps.tenant_apps.assets",
        "home_erp.apps.tenant_apps.chores",
    ]
    for app in expected_apps:
        assert app in settings.INSTALLED_APPS
        assert apps.is_installed(app)


def test_no_legacy_b2b_apps_installed():
    """Verify that legacy fasbot / B2B apps and core app are excluded."""
    forbidden_apps = [
        "core",
        "chatbots",
        "crm",
        "pos",
        "sales",
        "fabrication",
        "taxes",
        "rental",
        "returns",
        "procurement",
        "quality",
        "cashbox",
    ]
    installed_app_names = [app.split(".")[-1] for app in settings.INSTALLED_APPS]
    for forbidden in forbidden_apps:
        assert forbidden not in installed_app_names
