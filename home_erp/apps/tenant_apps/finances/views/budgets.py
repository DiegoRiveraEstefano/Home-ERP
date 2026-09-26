"""Views for budgets in finances."""

from django.views.generic import TemplateView


class BudgetsDashboardView(TemplateView):
    """Controller view for budgets."""
    template_name = "finances/budgets.html"
