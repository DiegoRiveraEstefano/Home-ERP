# Documentation Standards (DOCS.md)

Home-ERP maintains its single source of truth for technical architecture, domain specifications, and ADRs under the `/docs` directory using [Sphinx](https://www.sphinx-doc.org/) and reStructuredText (`.rst`).

## Directory Layout

```text
docs/
├── conf.py                   # Sphinx build configuration
├── index.rst                 # Master root toctree
├── architecture/             # Architectural overviews and patterns
│   ├── index.rst
│   ├── overview.rst
│   ├── household-tenancy.rst
│   ├── service-layer.rst
│   └── adr/                  # Architecture Decision Records
│       ├── index.rst
│       └── *.rst
├── specs/                    # Domain functional specifications
│   ├── index.rst
│   ├── households.rst
│   ├── finances.rst
│   ├── inventory.rst
│   ├── assets_maintenance.rst
│   └── chores_tasks.rst
└── development/              # Setup, coding, and testing guides
    ├── index.rst
    ├── setup.rst
    └── testing.rst
```

## Documentation Guidelines

1. **No Orphan Files**: Every `.rst` document must be included in the corresponding `toctree` of its parent `index.rst`. Unindexed files fail the documentation build.
2. **Google-Style Docstrings**: All Python functions, classes, and service methods must include Google-style docstrings (`Args:`, `Returns:`, `Raises:`).
3. **Neutral Technical Language**: Write concisely, avoid filler words, and state technical decisions objectively.
4. **Living Documentation**: When code changes modify domain behaviors, service arguments, or model attributes, update the documentation in the same change cycle.

## Building Documentation Locally

```bash
# Install docs dependencies
uv pip install sphinx furo sphinx-autobuild

# Build static HTML documentation
cd docs && uv run sphinx-build -b html . _build/html

# Live reload during authoring
uv run sphinx-autobuild docs docs/_build/html
```
