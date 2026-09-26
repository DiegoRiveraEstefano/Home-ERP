"""Views for audit_logs in audit."""

from django.views.generic import TemplateView


class AuditLogsDashboardView(TemplateView):
    """Controller view for audit_logs."""
    template_name = "audit/audit_logs.html"
