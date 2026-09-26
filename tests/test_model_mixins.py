import uuid

from home_erp.shared.models import ActiveStatusModelMixin
from home_erp.shared.models import BaseModel
from home_erp.shared.models import HouseholdScopedModel
from home_erp.shared.models import HouseholdScopedModelMixin
from home_erp.shared.models import SoftDeleteModelMixin
from home_erp.shared.models import TimeStampedModelMixin
from home_erp.shared.models import UUIDv7ModelMixin

UUIDV7_VERSION = 7


class DummyDomesticModel(
    HouseholdScopedModel,
    ActiveStatusModelMixin,
    SoftDeleteModelMixin,
):
    """Concrete dummy model for unit testing shared mixins without database."""

    class Meta:
        app_label = "users"


def test_uuidv7_mixin_generates_valid_uuid():
    """Verify UUIDv7ModelMixin defaults to a valid UUIDv7."""
    instance = DummyDomesticModel(household_id=uuid.uuid4())
    # Field default generates uuid7
    assert instance.id is not None
    assert isinstance(instance.id, uuid.UUID)
    assert instance.id.version == UUIDV7_VERSION


def test_household_scoped_mixin_requires_household():
    """Verify HouseholdScopedModel stores household_id."""
    test_household_id = uuid.uuid4()
    instance = DummyDomesticModel(household_id=test_household_id)
    assert instance.household_id == test_household_id


def test_active_status_mixin_default():
    """Verify ActiveStatusModelMixin defaults to True."""
    instance = DummyDomesticModel(household_id=uuid.uuid4())
    assert instance.is_active is True


def test_soft_delete_mixin_methods():
    """Verify SoftDeleteModelMixin properties and methods."""
    instance = DummyDomesticModel(household_id=uuid.uuid4())
    assert instance.is_deleted is False
    assert instance.deleted_at is None

    # Test soft delete field mutation
    instance.is_deleted = True
    assert instance.is_deleted is True


def test_inheritance_hierarchy():
    """Verify mixin class hierarchy."""
    assert issubclass(BaseModel, (UUIDv7ModelMixin, TimeStampedModelMixin))
    assert issubclass(HouseholdScopedModel, (BaseModel, HouseholdScopedModelMixin))
