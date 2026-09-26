# Build stage: compile dependencies using Astral uv
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS python-build-stage

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# System build dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependency synchronization
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
        --frozen \
        --no-dev \
        --no-install-project

# Source code copying
COPY README.md ./
COPY home_erp ./home_erp
COPY config ./config
COPY manage.py ./

# Project self-installation
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
        --frozen \
        --no-dev

# Final runtime stage
FROM python:3.14-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings.production

# Runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Unprivileged system user
RUN addgroup --system home_erp && adduser --system --ingroup home_erp home_erp

# Copy virtual environment and project files
COPY --from=python-build-stage --chown=home_erp:home_erp /app/.venv /app/.venv
COPY --chown=home_erp:home_erp . .

# Runtime directories and entrypoint
COPY --chown=home_erp:home_erp compose/django/entrypoint.sh /entrypoint
RUN install -d -m 0755 -o home_erp -g home_erp /app/staticfiles /app/media /app/logs && \
    sed -i 's/\r$//g' /entrypoint && \
    chmod +x /entrypoint

USER home_erp

ENTRYPOINT ["/entrypoint"]

CMD ["granian", "--interface", "wsgi", "config.wsgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--blocking-threads", "8", "--runtime-mode", "mt"]
