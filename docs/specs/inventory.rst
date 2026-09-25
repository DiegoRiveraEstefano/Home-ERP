Inventory & Pantry Domain Specification
========================================

Overview
--------
The Inventory domain enables domestic item tracking, stock auditing, expiration date management, and shopping list generation.

Core Models
-----------

StorageLocation
~~~~~~~~~~~~~~~
Identifies where items are kept within the household.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``name``: Location name (e.g., "Kitchen Pantry", "Upstairs Freezer", "Laundry Cabinet").
* ``description``: Text.

ItemCategory
~~~~~~~~~~~~
Domestic taxonomy for grouping items.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``name``: Category name (e.g., "Dairy", "Spices", "Canned Goods", "Cleaning Supplies").

PantryItem
~~~~~~~~~~
The conceptual catalog of an item tracked by the household.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``name``: Item title (e.g., "Whole Milk 1L", "Olive Oil", "Dish Soap").
* ``barcode``: Optional barcode / UPC string for quick mobile scanning.
* ``category``: ForeignKey to ``ItemCategory``.
* ``default_location``: ForeignKey to ``StorageLocation``.
* ``unit_of_measure``: ChoiceField (``GRAMS``, ``KILOGRAMS``, ``MILLILITERS``, ``LITERS``, ``PIECES``).
* ``minimum_threshold``: DecimalField (triggers automated addition to shopping list).
* ``current_stock``: DecimalField (computed aggregated stock from active batches).

StockBatch
~~~~~~~~~~
Specific physical lot of an item, tracking purchase date and expiration.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``item``: ForeignKey to ``PantryItem``.
* ``location``: ForeignKey to ``StorageLocation``.
* ``quantity``: DecimalField.
* ``expiration_date``: Date.
* ``opened_at``: Optional date when the container was opened.
* ``purchase_date``: Optional purchase date.

ShoppingListItem
~~~~~~~~~~~~~~~~
Tracks domestic items required for replenishment.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``item``: Optional ForeignKey to ``PantryItem`` (null for custom one-off items).
* ``custom_name``: Optional string for ad-hoc items not yet in the catalog.
* ``desired_quantity``: DecimalField.
* ``is_purchased``: Boolean flag.
* ``added_by``: ForeignKey to ``users.User``.

Public Services
---------------

* ``InventoryService.add_stock(household_id, item_id, location_id, quantity, expiration_date)``
* ``InventoryService.consume_stock(household_id, batch_id, quantity, user)``
* ``InventoryService.generate_replenishment_list(household_id)``: Scans items where current stock <= minimum threshold and adds to shopping list.
