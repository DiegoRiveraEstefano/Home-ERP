# Contributing to Home-ERP

Thank you for contributing to Home-ERP. Follow these guidelines to maintain code quality, architecture consistency, and testing discipline.

## Development Workflow

1. **Issue First**: Ensure every non-trivial change references a clear problem statement or task.
2. **Branch Naming**:
   - `feature/<short-desc>` (e.g., `feature/pantry-barcode-lookup`)
   - `bugfix/<short-desc>` (e.g., `bugfix/expense-rounding-error`)
   - `chore/<short-desc>` (e.g., `chore/bump-django-version`)
3. **Branch Protection**: Never commit directly to `main`. Create feature branches and submit pull requests.

## Commit Standards

Home-ERP adheres to the [Conventional Commits](https://www.conventionalcommits.org/) specification:

Format:
```text
<type>(<scope>): <short imperative description>

- Detailed bullet point explaining rationale
- Another technical detail or reference
```

Allowed types:
- `feat`: New user or system capabilities
- `fix`: Bug resolution
- `docs`: Documentation updates
- `style`: Formatting, missing semicolons, whitespace
- `refactor`: Code restructuring without behavioral change
- `perf`: Performance improvements
- `test`: Adding or refactoring tests
- `chore`: Maintenance, dependencies, tooling

Common scopes: `finances`, `inventory`, `assets`, `chores`, `households`, `core`, `docs`.

## Pull Request Checklist

Before submitting a pull request:
1. Run tests and verify all pass: `uv run pytest`.
2. Ensure no N+1 query regressions in views or selectors.
3. Verify test coverage for new business services.
4. Keep diffs focused: avoid modifying unrelated code.
5. Update documentation in `/docs` if APIs, models, or service signatures change.
