"""Views for pantry in inventory."""

from django.views.generic import TemplateView


class PantryDashboardView(TemplateView):
    """Controller view for pantry."""
    template_name = "inventory/pantry.html"
