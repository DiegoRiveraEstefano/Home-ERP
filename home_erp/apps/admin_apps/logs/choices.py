"""Enums and choices for admin_logs."""
from django.db import models

class LogLevel(models.TextChoices):
    DEBUG = "DEBUG", "Debug"
    INFO = "INFO", "Info"
    WARNING = "WARNING", "Warning"
    ERROR = "ERROR", "Error"
    CRITICAL = "CRITICAL", "Critical"

