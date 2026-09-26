# Resumen de Cambios: Limpieza de Configuraciones y Organización Modular de Apps

Fecha: 2026-09-25

## Cambios Realizados
- **Mixins de Modelos Genéricos (`home_erp/shared/models/`)**:
  - Implementado `UUIDv7ModelMixin` utilizando `uuid6.uuid7` para claves primarias ordenadas temporalmente.
  - Implementado `TimeStampedModelMixin` con campos indexados `created_at` y `updated_at`.
  - Implementado `HouseholdScopedModelMixin` con campo `household_id` indexado para aislamiento estricto de datos del hogar.
  - Implementado `ActiveStatusModelMixin` con campo booleano `is_active`.
  - Implementado `SoftDeleteModelMixin` con `is_deleted`, `deleted_at` y métodos `soft_delete()` y `restore()`.
  - Creados modelos abstractos base compuestos: `BaseModel` (UUIDv7 + Timestamps) y `HouseholdScopedModel` (BaseModel + Household Scoping).
  - Exportados todos los mixins en `home_erp/shared/models/__init__.py`.
- **Eliminación de la Aplicación `core`**:
  - Eliminado el directorio `home_erp/apps/common_apps/core/`.
  - Removido `"home_erp.apps.common_apps.core"` de `LOCAL_APPS` en `config/settings/base.py`.
- **Reorganización Categórica de `home_erp/apps/`**:
  - `home_erp/apps/common_apps/`: Aplicaciones transversales (`users` con `User(AbstractUser)`).
  - `home_erp/apps/tenant_apps/`: Bounded contexts del hogar (`households`, `finances`, `inventory`, `assets`, `chores`).
  - `home_erp/apps/admin_apps/`: Espacio reservado para herramientas administrativas.
- **Recreación de `home_erp/shared/`**:
  - Recreado el paquete compartido con sus submódulos utilitarios: `logging`, `models`, `fields`, `operations`, `pagination`, `services`, `templatetags`, `utils`, `validators`, `value_objects`, `exceptions`, `filters`, `tenancy`, `cache`, `constants`.
- **Configuración Django (`config/settings/`)**:
  - Depurado `LOCAL_APPS` en `base.py` con los módulos finales.
  - Purgadas referencias residuales a fasbot y B2B (`chatbots`, `crm`, tareas de leads, etc.).
  - Configurado logging estándar de Python en lugar de `structlog`.
- **Suite de Pruebas (`tests/`)**:
  - Reubicada suite de pruebas a `tests/` en la raíz del repositorio.
  - Creado `tests/test_installed_apps.py` (valida apps instaladas y exclusión de apps legadas).
  - Creado `tests/test_model_mixins.py` (valida generación de UUIDv7, scoping de household, timestamps, status y soft delete).
  - Validación con `manage.py check`, `pytest` y `ruff check`.
