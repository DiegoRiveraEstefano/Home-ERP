Chores & Tasks Domain Specification
===================================

Overview
--------
The Chores domain automates domestic labor coordination, task assignments, routine domestic maintenance, and accountability among household members.

Core Models
-----------

Chore
~~~~~
Defines a repeating or one-off household chore.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``title``: Task name (e.g., "Empty Dishwasher", "Vacuum Living Room", "Take Out Trash").
* ``description``: Guidance instructions.
* ``frequency``: ChoiceField (``DAILY``, ``WEEKLY``, ``BIWEEKLY``, ``MONTHLY``, ``ONCE``).
* ``points``: Integer reward weight or gamification score.
* ``rotation_enabled``: Boolean (True if chore rotates automatically among members).
* ``default_assignee``: Optional ForeignKey to ``users.User``.

ChoreAssignment
~~~~~~~~~~~~~~~
An instance of a chore scheduled for execution.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``chore``: ForeignKey to ``Chore``.
* ``assigned_to``: ForeignKey to ``users.User``.
* ``due_date``: Date.
* ``status``: ChoiceField (``PENDING``, ``COMPLETED``, ``OVERDUE``, ``SKIPPED``).
* ``completed_at``: Optional timestamp.
* ``completed_by``: Optional ForeignKey to ``users.User``.

Public Services
---------------

* ``ChoreService.create_chore(household_id, data)``
* ``ChoreService.generate_daily_assignments(household_id, target_date)``
* ``ChoreService.complete_assignment(household_id, assignment_id, completed_by)``
* ``ChoreService.rotate_assignee(chore_id)``
