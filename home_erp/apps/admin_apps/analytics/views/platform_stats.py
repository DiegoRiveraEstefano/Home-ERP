"""Views for platform_stats in admin_analytics."""

from django.views.generic import TemplateView


class PlatformStatsDashboardView(TemplateView):
    """Controller view for platform_stats."""
    template_name = "admin_analytics/platform_stats.html"
