"""Views for exports in exports."""

from django.views.generic import TemplateView


class ExportsDashboardView(TemplateView):
    """Controller view for exports."""
    template_name = "exports/exports.html"
