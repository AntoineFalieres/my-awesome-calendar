---
name: roadmap-todo-changelog-auto-updater
description: Update ROADMAP.md, TODO.md, and CHANGELOG.md automatically from merged PR metadata using deterministic role ownership rules.
---

# Roadmap/TODO/Changelog Auto Updater

Use this skill when the repository needs automatic documentation synchronization
after merged pull requests.

## Quick Start

Generate updates locally from a prepared PR metadata JSON payload:

```bash
python3 \
  .github/agentic/skills/project/roadmap-todo-changelog-auto-updater/scripts/update_docs_from_pr.py \
  --pr-json /tmp/merged_pr.json
```

Dry-run without writing files:

```bash
python3 \
  .github/agentic/skills/project/roadmap-todo-changelog-auto-updater/scripts/update_docs_from_pr.py \
  --pr-json /tmp/merged_pr.json \
  --dry-run
```

## Required Behavior

- Read merged PR metadata (number, title, body, URL, merged date, changed files).
- Infer agent-role ownership deterministically using explicit rules:
  - PM
  - SEO
  - UX/UI
  - Full-Stack
  - Ad Ops
- Update only dedicated auto-managed sections in:
  - `ROADMAP.md`
  - `TODO.md`
  - `CHANGELOG.md`
- Keep updates idempotent by PR number (and role for TODO lines).
- Never rewrite manual sections outside marker boundaries.

## Workflow

1. Collect merged PR metadata from GitHub.
2. Run the updater script against repository markdown files.
3. Review generated diffs for role mapping and entry quality.
4. Open a follow-up PR with only the managed doc updates.

## Review Checks

Before finalizing, confirm:

- Managed markers still exist and wrap generated content.
- Re-running the script for the same PR produces no duplicate entries.
- Role assignment is consistent with changed files and PR text.
- `ROADMAP.md`, `TODO.md`, and `CHANGELOG.md` remain valid markdown.

## Notes

- This skill is deterministic by design; no generative text expansion.
- If role mapping needs tuning, edit the keyword/path rules in the script.
