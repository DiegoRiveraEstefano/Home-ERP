"""Views for notifications in notifications."""

from django.views.generic import TemplateView


class NotificationsDashboardView(TemplateView):
    """Controller view for notifications."""
    template_name = "notifications/notifications.html"
