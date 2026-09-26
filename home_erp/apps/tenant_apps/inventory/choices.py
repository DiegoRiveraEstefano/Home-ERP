"""Enums and choices for inventory."""
from django.db import models

class UnitOfMeasure(models.TextChoices):
    GRAMS = "GRAMS", "Grams"
    KILOGRAMS = "KILOGRAMS", "Kilograms"
    MILLILITERS = "MILLILITERS", "Milliliters"
    LITERS = "LITERS", "Liters"
    PIECES = "PIECES", "Pieces"
    PACKS = "PACKS", "Packs"

