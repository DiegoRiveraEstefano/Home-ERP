"""Views for expenses in finances."""

from django.views.generic import TemplateView


class ExpensesDashboardView(TemplateView):
    """Controller view for expenses."""
    template_name = "finances/expenses.html"
