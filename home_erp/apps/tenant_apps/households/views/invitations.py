"""Views for invitations in households."""

from django.views.generic import TemplateView


class InvitationsDashboardView(TemplateView):
    """Controller view for invitations."""
    template_name = "households/invitations.html"
