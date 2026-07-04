---
name: technical-seo-checklist
description: Apply technical SEO best practices for rendered pages, including metadata quality, semantic structure, crawlability, indexability, and performance-aware implementation choices.
---

# Technical SEO Checklist

Use this skill when changing page templates, metadata, content structure, or
linking that can affect search discoverability.

## Quick Start

Run technical SEO checks across templates:

```bash
uv run python \
    .github/agentic/skills/seo/technical-seo-checklist/scripts/check_seo_templates.py
```

Fail the run when issues are found:

```bash
uv run python \
    .github/agentic/skills/seo/technical-seo-checklist/scripts/check_seo_templates.py \
    --fail-on-issues
```

## Required Behavior

- Ensure each user-facing page has a specific, non-placeholder title.
- Ensure each user-facing page has a meaningful meta description.
- Maintain semantic heading hierarchy and avoid skipped heading levels.
- Keep key content server-rendered and crawlable.
- Ensure internal links use valid anchor tags with stable URLs.
- Avoid introducing duplicate canonical targets or conflicting metadata.

## Workflow

1. Identify which routes/pages are SEO-impacting.
2. Inspect template head metadata and heading structure.
3. Add or adjust metadata (`title`, description, canonical when relevant).
4. Verify links and page structure support crawlability.
5. Confirm changes do not degrade initial render performance.

## Review Checks

Before finalizing, confirm:

- Page title and meta description are present and specific.
- Heading hierarchy is logical (`h1` then structured subsections).
- Canonical usage is correct for pages where duplicate URLs are possible.
- New links are discoverable and not JS-only.
- No SEO-critical fields are left as placeholder text.
- `check_seo_templates.py` reports no unresolved issues (or issues are
  explicitly accepted by the user).

## Best Practices

- Write title tags for intent and clarity first, then optimize length.
- Keep descriptions specific to the page value; avoid generic boilerplate.
- Prefer stable URLs and avoid unnecessary duplicate routes.
- Keep legal/privacy pages indexable unless there is a clear policy reason not
  to.
- When adding new public pages, link them from at least one crawlable page.

## Notes

- Prefer practical, measurable SEO improvements over speculative additions.
- When a request is purely backend/API-only, do not force SEO changes that do
  not affect rendered pages.
