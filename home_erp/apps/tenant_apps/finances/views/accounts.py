"""Views for accounts in finances."""

from django.views.generic import TemplateView


class AccountsDashboardView(TemplateView):
    """Controller view for accounts."""
    template_name = "finances/accounts.html"
