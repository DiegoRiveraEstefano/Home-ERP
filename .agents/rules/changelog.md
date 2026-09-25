---
trigger: always_on
---

# Home-ERP: Changelog Guidelines

## Change Cycle Summaries
- For each completed set of changes (feature, bugfix, hotfix, chore), create a summary file in `docs/changes/`.
- Naming: `<short-description>-<YYYY-MM-DD>.md` (e.g., `pantry-batch-expiry-2026-09-25.md`).
- Content: bullet list of key changes, referencing tickets, PRs, or domestic modules.

## `CHANGELOG.md` Aggregation
- `CHANGELOG.md` (root) is the project-level changelog.
- Do not manually edit it for every minor change.
- On release or on demand, merge selected summaries from `docs/changes/` into `CHANGELOG.md` under a version header (e.g., `## [0.2.0] - 2026-10-01`).
- Maintain consistent structure following Keep a Changelog.

## Anti-patterns vs. Best Practices

| Anti-pattern | Correct |
|---|---|
| Directly editing `CHANGELOG.md` for every minor change | Create a dated summary file in `docs/changes/`; aggregate on release |
| Omitting a summary after a significant change cycle | Always produce a `docs/changes/` file immediately |
| Inconsistent naming of summary files | `<description>-<YYYY-MM-DD>.md` |