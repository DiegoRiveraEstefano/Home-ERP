"""Reusable abstract model mixins for Home-ERP domestic domain models."""

import uuid6
from django.db import models
from django.utils import timezone


class UUIDv7ModelMixin(models.Model):
    """Abstract model mixin providing a time-ordered UUIDv7 primary key."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid6.uuid7,
        editable=False,
        help_text="Time-ordered UUIDv7 primary key.",
    )

    class Meta:
        abstract = True


class TimeStampedModelMixin(models.Model):
    """Abstract model mixin providing creation and modification timestamps."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when this record was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last modified.",
    )

    class Meta:
        abstract = True


class HouseholdScopedModelMixin(models.Model):
    """Abstract model mixin ensuring multi-household isolation and data scoping."""

    household_id = models.UUIDField(
        db_index=True,
        editable=False,
        help_text="Mandatory Household UUID for domestic tenancy isolation.",
    )

    class Meta:
        abstract = True


class ActiveStatusModelMixin(models.Model):
    """Abstract model mixin providing an active status toggle."""

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Designates whether this record is considered active.",
    )

    class Meta:
        abstract = True


class SoftDeleteModelMixin(models.Model):
    """Abstract model mixin providing soft delete functionality with timestamps."""

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Designates whether this record has been marked as deleted.",
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when this record was soft-deleted.",
    )

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Mark record as soft-deleted."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self) -> None:
        """Restore soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class BaseModel(UUIDv7ModelMixin, TimeStampedModelMixin):
    """Abstract base model combining UUIDv7 primary key and timestamp tracking."""

    class Meta:
        abstract = True


class HouseholdScopedModel(BaseModel, HouseholdScopedModelMixin):
    """Abstract base model combining UUIDv7, timestamps, and tenancy scoping."""

    class Meta:
        abstract = True
