Households Domain Specification
===============================

Overview
--------
The Households domain acts as the root boundary for tenancy and identity within Home-ERP. It manages household entities, user memberships, invitation links, and role assignments.

Core Models
-----------

Household
~~~~~~~~~
Represents a domestic group or family living unit.

* ``id``: UUIDv7 primary key.
* ``name``: Human-readable name (e.g., "The Rivera Household").
* ``currency``: Default ISO currency code (e.g., ``USD``, ``CLP``, ``EUR``).
* ``timezone``: Active timezone string (e.g., ``America/Santiago``).
* ``created_at``: Timestamp.
* ``updated_at``: Timestamp.

HouseholdMember
~~~~~~~~~~~~~~~
Associates a Django User with a Household and assigns access privileges.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``user``: ForeignKey to ``users.User``.
* ``role``: ChoiceField:
  * ``OWNER``: Full control over settings, members, finances, and data exports.
  * ``MEMBER``: Can record transactions, manage pantry items, and complete tasks.
  * ``GUEST``: Limited read-only visibility into pantry items and assigned chores.
* ``joined_at``: Timestamp.

HouseholdInvitation
~~~~~~~~~~~~~~~~~~~
Allows existing owners to invite new members via secure one-time tokens.

* ``id``: UUIDv7 primary key.
* ``household``: ForeignKey to ``Household``.
* ``email``: Invitee email address.
* ``role``: Target role.
* ``token``: Secure cryptographic string.
* ``expires_at``: Expiration timestamp.
* ``is_accepted``: Boolean flag.

Public Services
---------------

* ``HouseholdService.create_household(user, name, currency, timezone)``: Creates a household and enrolls the user as ``OWNER``.
* ``HouseholdService.invite_member(household_id, invited_by, email, role)``: Issues an email invitation.
* ``HouseholdService.accept_invitation(token, user)``: Validates token and creates ``HouseholdMember`` record.
