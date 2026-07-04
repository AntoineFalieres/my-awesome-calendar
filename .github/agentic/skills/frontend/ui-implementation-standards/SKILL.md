---
name: ui-implementation-standards
description: Implement or refactor frontend behavior in templates with consistent responsiveness, accessibility, and maintainable JavaScript patterns. Use when changing HTML/CSS/JS in rendered pages.
---

# UI Implementation Standards

Use this skill when implementing or reviewing frontend changes in this
repository.

## Quick Start

Run the frontend template checks:

```bash
uv run python \
    .github/agentic/skills/frontend/ui-implementation-standards/scripts/check_ui_templates.py
```

Fail the run when issues are found:

```bash
uv run python \
    .github/agentic/skills/frontend/ui-implementation-standards/scripts/check_ui_templates.py \
    --fail-on-issues
```

## Required Behavior

- Base UI changes on existing Flask-rendered templates under `templates/`.
- Preserve core calendar interactions unless the user explicitly requests
  behavior changes.
- Keep layouts responsive for small and large screens.
- Prefer semantic HTML and maintain accessible labels and controls.
- Keep JavaScript clear, scoped, and resilient to fetch failures.
- Avoid duplicating client-side request logic when a shared function can be
  reused.

## Workflow

1. Identify the user flow impacted by the UI change.
2. Locate the template and script blocks involved.
3. Apply minimal, explicit HTML/CSS/JS edits that solve the request.
4. Ensure selectors, listeners, and API routes remain aligned.
5. Re-check responsive structure and accessibility labels.

## Review Checks

Before finalizing, confirm:

- Controls remain usable with keyboard and screen-reader-friendly labels.
- Existing country/year/subdivision/zone flows still work as intended.
- Error paths do not leave stale or misleading UI state.
- Markup and script changes are understandable and not over-coupled.
- `check_ui_templates.py` reports no unresolved issues (or issues are explicitly
  accepted by the user).

## Best Practices

- Prefer progressive enhancement: baseline HTML should still communicate key
  information before JavaScript runs.
- Keep DOM queries and listeners close to where state changes happen.
- Reuse helpers for repeated fetch and error handling paths.
- Minimize inline styles; prefer class-based styling for maintainability.
- Keep copy and labels explicit and user-facing (avoid ambiguous placeholders).

## Notes

- Keep CDN dependency usage consistent with current project style unless a
  dependency migration is requested.
- For broad UI redesigns, prefer incremental changes over large rewrites.
