"""Enums and choices for admin_backups."""
from django.db import models

class BackupStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"

