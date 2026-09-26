"""Views for backups in admin_backups."""

from django.views.generic import TemplateView


class BackupsDashboardView(TemplateView):
    """Controller view for backups."""
    template_name = "admin_backups/backups.html"
