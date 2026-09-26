## Description

<!-- Brief summary of changes, rationale, and related issues -->

Closes #

## Type of Change

- [ ] `feat`: New capability or feature
- [ ] `fix`: Bug fix
- [ ] `refactor`: Code restructuring without functional change
- [ ] `perf`: Performance improvement
- [ ] `test`: Adding or updating test suite
- [ ] `docs`: Documentation updates in `docs/`
- [ ] `chore`: Maintenance, dependencies, or tooling

## Domain Scope

- [ ] `finances`
- [ ] `inventory`
- [ ] `assets`
- [ ] `chores`
- [ ] `households`
- [ ] `core`
- [ ] `docs` / other

## Architectural & Domain Checklist

- [ ] **Domestic Scope**: Adheres strictly to domestic boundaries (no enterprise/B2B patterns).
- [ ] **Household Isolation**: All service methods and queries explicitly scoped by `household_id`.
- [ ] **Service Layer**: Mutations and workflows located in `services/` (`@classmethod` wrapped in `transaction.atomic()`).
- [ ] **Selector Layer**: Read queries, aggregations, and prefetching located in `selectors.py` (no business logic or mutations).
- [ ] **Thin Controllers**: Views only unpack parameters, delegate to services/selectors, and return responses.
- [ ] **Frontend**: Native HTML semantics, Warm Hearth Vanilla CSS tokens (`@layer`), Unpoly fragments without external JS frameworks.

## Quality Checklist

- [ ] Tests pass locally (`uv run pytest`).
- [ ] Linter and format pass (`uv run ruff check .` and `uv run ruff format --check .`).
- [ ] No N+1 query regressions (`django_assert_max_num_queries` used where applicable).
- [ ] Documentation updated in `/docs` if models, service signatures, or specs changed.
- [ ] Change summary recorded in `docs/changes/<desc>-<YYYY-MM-DD>.md` if applicable.
- [ ] Commits follow Conventional Commits (`type(scope): description`).
