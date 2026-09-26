FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS build

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --only-group docs --no-install-project && \
    uv pip install furo

FROM python:3.14-slim AS runner

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

COPY --from=build /app/.venv /app/.venv
COPY . .

EXPOSE 9000

CMD ["sphinx-autobuild", "docs", "docs/_build/html", "--host", "0.0.0.0", "--port", "9000"]
