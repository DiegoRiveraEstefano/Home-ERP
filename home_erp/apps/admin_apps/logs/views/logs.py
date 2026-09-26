"""Views for logs in admin_logs."""

from django.views.generic import TemplateView


class LogsDashboardView(TemplateView):
    """Controller view for logs."""
    template_name = "admin_logs/logs.html"
