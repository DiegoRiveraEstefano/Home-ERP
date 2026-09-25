# Changelog

All notable changes to the Home-ERP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Shifted frontend architecture from Tailwind CSS to Modern Vanilla CSS (`@layer`, custom properties, CSS Grid, container queries).
- Adopted Unpoly for server-driven interactions and fragment updates.
- Replaced client runtime state with native Vanilla JS and Web Components.
- Standardized templates on built-in Django template rendering (`{% include %}`, `{% block %}`).
- Standardized logging on Python native `logging` configured via Django settings.

### Added
- Architectural notes adaptation from `notas/v2` to domestic Python/Django structure.
- Complete technical documentation in `/docs` using Sphinx `.rst` format.
- Root governance specifications (`AGENTS.md`, `CONTEXT.md`, `CONTRIBUTING.md`, `DOCS.md`, `GUIDELINES.md`, `SECURITY.md`, `STYLE_GUIDE.md`).
- Domain specifications for households, finances, inventory/pantry, assets/maintenance, and chores.
- Agent operational rules in `.agents/rules/` aligned to Home-ERP.

## [0.1.0] - 2026-09-25

### Added
- Project repository initialization with `uv` and Python 3.12+ baseline.
