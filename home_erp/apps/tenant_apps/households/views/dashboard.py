"""Views for dashboard in households."""

from django.views.generic import TemplateView


class DashboardDashboardView(TemplateView):
    """Controller view for dashboard."""
    template_name = "households/dashboard.html"
