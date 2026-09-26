"""Views for chores in chores."""

from django.views.generic import TemplateView


class ChoresDashboardView(TemplateView):
    """Controller view for chores."""
    template_name = "chores/chores.html"
