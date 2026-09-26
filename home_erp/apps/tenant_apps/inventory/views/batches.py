"""Views for batches in inventory."""

from django.views.generic import TemplateView


class BatchesDashboardView(TemplateView):
    """Controller view for batches."""
    template_name = "inventory/batches.html"
