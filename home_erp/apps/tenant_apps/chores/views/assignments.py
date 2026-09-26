"""Views for assignments in chores."""

from django.views.generic import TemplateView


class AssignmentsDashboardView(TemplateView):
    """Controller view for assignments."""
    template_name = "chores/assignments.html"
