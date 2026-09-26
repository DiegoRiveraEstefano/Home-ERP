"""Enums and choices for exports."""
from django.db import models

class ExportFormat(models.TextChoices):
    JSON = "JSON", "JSON"
    CSV = "CSV", "CSV"
    PDF = "PDF", "PDF"

