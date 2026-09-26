"""Views for profile in users."""

from django.views.generic import TemplateView


class ProfileDashboardView(TemplateView):
    """Controller view for profile."""
    template_name = "users/profile.html"
