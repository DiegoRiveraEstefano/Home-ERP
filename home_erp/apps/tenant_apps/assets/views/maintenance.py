"""Views for maintenance in assets."""

from django.views.generic import TemplateView


class MaintenanceDashboardView(TemplateView):
    """Controller view for maintenance."""
    template_name = "assets/maintenance.html"
