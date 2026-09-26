"""Enums and choices for audit."""
from django.db import models

class AuditCategory(models.TextChoices):
    MEMBERSHIP = "MEMBERSHIP", "Membership"
    INVENTORY = "INVENTORY", "Inventory"
    FINANCES = "FINANCES", "Finances"
    CHORES = "CHORES", "Chores"
    ASSETS = "ASSETS", "Assets"
    SETTINGS = "SETTINGS", "Settings"

