"""Views for analytics in tenant_analytics."""

from django.views.generic import TemplateView


class AnalyticsDashboardView(TemplateView):
    """Controller view for analytics."""
    template_name = "tenant_analytics/analytics.html"
