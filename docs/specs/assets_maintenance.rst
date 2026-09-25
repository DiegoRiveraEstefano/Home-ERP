Assets & Maintenance Domain Specification
==========================================

Overview
--------
The Assets domain catalogs domestic durable goods, appliances, vehicles, and electronics, managing their warranties, instruction manuals, and preventative maintenance schedules.

Core Models
-----------

Asset
~~~~~
Represents a physical device or durable property belonging to the household.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``name``: Label (e.g., "Bosch Dishwasher Series 4", "LG OLED TV", "Lawnmower").
* ``brand``: Brand/manufacturer name.
* ``model_number``: Manufacturer model string.
* ``serial_number``: Hardware serial code.
* ``purchase_date``: Date.
* ``purchase_price``: Optional DecimalField.
* ``warranty_expiration``: Optional Date.
* ``manual_file``: Optional FileField for PDF manual.
* ``receipt_file``: Optional FileField for proof of purchase.
* ``location``: ForeignKey to ``inventory.StorageLocation``.

MaintenanceSchedule
~~~~~~~~~~~~~~~~~~~
Recurring maintenance requirements for an asset.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``asset``: ForeignKey to ``Asset``.
* ``title``: Action description (e.g., "Replace HEPA Filter", "Clean Filter & Descale").
* ``frequency_days``: Interval in days between services.
* ``last_performed_date``: Date.
* ``next_due_date``: Date.

MaintenanceLog
~~~~~~~~~~~~~~
Historical record of performed maintenance, servicing, or repairs.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``asset``: ForeignKey to ``Asset``.
* ``schedule``: Optional ForeignKey to ``MaintenanceSchedule``.
* ``performed_date``: Date.
* ``performed_by``: Optional ForeignKey to ``users.User`` or external service provider string.
* ``cost``: Optional DecimalField.
* ``notes``: Detailed description of actions taken.

Public Services
---------------

* ``AssetService.register_asset(household_id, data, files)``
* ``AssetService.log_maintenance(household_id, asset_id, schedule_id, cost, notes, user)``
* ``AssetService.calculate_upcoming_maintenance(household_id)``
