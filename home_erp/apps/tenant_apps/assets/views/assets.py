"""Views for assets in assets."""

from django.views.generic import TemplateView


class AssetsDashboardView(TemplateView):
    """Controller view for assets."""
    template_name = "assets/assets.html"
