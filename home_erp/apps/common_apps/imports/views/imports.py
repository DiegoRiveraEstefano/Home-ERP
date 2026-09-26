"""Views for imports in imports."""

from django.views.generic import TemplateView


class ImportsDashboardView(TemplateView):
    """Controller view for imports."""
    template_name = "imports/imports.html"
