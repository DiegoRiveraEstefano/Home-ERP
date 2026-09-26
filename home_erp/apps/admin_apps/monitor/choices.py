"""Enums and choices for admin_monitor."""
from django.db import models

class HealthStatus(models.TextChoices):
    HEALTHY = "HEALTHY", "Healthy"
    DEGRADED = "DEGRADED", "Degraded"
    UNHEALTHY = "UNHEALTHY", "Unhealthy"

