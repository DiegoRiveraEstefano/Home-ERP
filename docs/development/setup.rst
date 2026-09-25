Local Environment Setup
=======================

Prerequisites
-------------
* Python 3.12 or newer.
* ``uv`` package installer and environment manager.
* Docker and Docker Compose (to run local PostgreSQL and Redis).

Initial Setup Steps
-------------------

1. **Clone the Repository**:

   .. code-block:: bash

       git clone https://github.com/DiegoRiveraEstefano/Home-ERP.git
       cd Home-ERP

2. **Sync Dependencies with uv**:

   .. code-block:: bash

       uv sync

3. **Start Backing Services**:

   .. code-block:: bash

       docker compose -f docker-compose.local.yml up -d

4. **Apply Migrations**:

   .. code-block:: bash

       uv run python manage.py migrate

5. **Create Superuser**:

   .. code-block:: bash

       uv run python manage.py createsuperuser

6. **Start Development Server**:

   .. code-block:: bash

       uv run python manage.py runserver

Environment Configuration
-------------------------
Configuration is managed via ``.env`` in the project root:

.. code-block:: ini

    DJANGO_DEBUG=True
    DJANGO_SECRET_KEY=local-dev-insecure-key
    DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/home_erp
    REDIS_URL=redis://127.0.0.1:6379/0
