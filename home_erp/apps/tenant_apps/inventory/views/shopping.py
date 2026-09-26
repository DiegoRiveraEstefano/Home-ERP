"""Views for shopping in inventory."""

from django.views.generic import TemplateView


class ShoppingDashboardView(TemplateView):
    """Controller view for shopping."""
    template_name = "inventory/shopping.html"
