"""Views for metrics in admin_metrics."""

from django.views.generic import TemplateView


class MetricsDashboardView(TemplateView):
    """Controller view for metrics."""
    template_name = "admin_metrics/metrics.html"
