from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """Default custom user model for Home-ERP."""

    name = models.CharField("Name of User", blank=True, max_length=255)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view."""
        return reverse("users:detail", kwargs={"username": self.username})
