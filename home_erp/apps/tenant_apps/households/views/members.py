"""Views for members in households."""

from django.views.generic import TemplateView


class MembersDashboardView(TemplateView):
    """Controller view for members."""
    template_name = "households/members.html"
