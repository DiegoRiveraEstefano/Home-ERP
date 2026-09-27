"""Form mixins for domestic tenancy scoping and data hygiene."""

import uuid
from typing import Any
from typing import override

from django import forms

from home_erp.shared.tenancy import get_current_household_id


class HouseholdScopedFormMixin:
    """Mixin for ModelForms ensuring choices and instances are scoped to household."""

    household_id: uuid.UUID | None

    def __init__(
        self,
        *args: Any,
        household_id: uuid.UUID | str | None = None,
        **kwargs: Any,
    ) -> None:
        raw_id = household_id or get_current_household_id()
        if raw_id is not None:
            self.household_id = (
                raw_id if isinstance(raw_id, uuid.UUID) else uuid.UUID(str(raw_id))
            )
        else:
            self.household_id = None

        super().__init__(*args, **kwargs)

        if self.household_id is not None:
            self._scope_choice_fields()

    def _scope_choice_fields(self) -> None:
        """Filter ModelChoiceField querysets to match household."""
        choice_classes = (forms.ModelChoiceField, forms.ModelMultipleChoiceField)
        for field in self.fields.values():
            if isinstance(field, choice_classes):
                model = field.queryset.model
                if hasattr(model, "household_id"):
                    field.queryset = field.queryset.filter(
                        household_id=self.household_id,
                    )

    @override
    def save(self, commit: bool = True) -> Any:
        if hasattr(super(), "save"):
            instance = super().save(commit=False)
        else:
            instance = getattr(self, "instance", None)

        if (
            instance is not None
            and self.household_id is not None
            and hasattr(instance, "household_id")
            and not instance.household_id
        ):
            instance.household_id = self.household_id

        if commit and instance is not None and hasattr(instance, "save"):
            instance.save()
            if hasattr(super(), "save_m2m"):
                super().save_m2m()
        return instance


class StripWhitespaceFormMixin:
    """Mixin that cleans CharField values in cleaned_data by stripping whitespace."""

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        if cleaned_data:
            for field_name, value in cleaned_data.items():
                if isinstance(value, str):
                    cleaned_data[field_name] = value.strip()
        return cleaned_data
