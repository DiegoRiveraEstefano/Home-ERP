---
trigger: always_on
---

# Home-ERP: Git Workflow

## Branch Safety
- Never delete or overwrite shared branches (`main`, `develop`).
- No force pushes on shared branches (`--force`, `--force-with-lease`).
- History rewrites (`rebase -i`, `amend` after push) allowed only on personal feature branches prior to PR review.

## Branch Naming
Create branches from latest `main`.
- `feature/<short-desc>` (e.g., `feature/pantry-expiration-alerts`)
- `bugfix/<short-desc>` (e.g., `bugfix/chore-rotation-edge-case`)
- `hotfix/<short-desc>`
- `chore/<short-desc>`

## Commit Messages (Conventional Commits)
Format: `<type>(<scope>): <imperative short description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`
- Scope: `finances`, `inventory`, `assets`, `chores`, `households`, `core`, `docs`
- Body mandatory: Detailed bullet list of changes for non-trivial commits.

Example:
```text
feat(finances): add monthly budget headroom validation

- Add limit checking in BudgetValidatorService
- Prevent expense creation exceeding category budget caps
- Add unit tests for budget violation edge cases
- Update finances domain specification in docs/specs/finances.rst
```

## Anti-patterns

| Incorrect | Correct |
|---|---|
| Commit directly to `main` | Feature branch + PR |
| Force push to shared branch | Never force push to shared branches |
| Vague commit title: `update code` | Conventional Commits + bullet list body |
| Multiple unrelated features in one branch | One branch per feature or bug |