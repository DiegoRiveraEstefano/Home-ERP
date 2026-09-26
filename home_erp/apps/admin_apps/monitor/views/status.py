"""Views for status in admin_monitor."""

from django.views.generic import TemplateView


class StatusDashboardView(TemplateView):
    """Controller view for status."""
    template_name = "admin_monitor/status.html"
