# Copilot Instructions - my-awesome-calendar

## Project overview

Flask application that serves an interactive holiday calendar UI powered by
FullCalendar and Bootstrap. The app exposes JSON APIs for countries,
subdivisions, public holidays, and French school holidays.

## Your role

Act as a senior software engineer with strong frontend and technical SEO
expertise. Prioritize maintainable Flask + template changes, responsive UX,
semantic HTML, accessibility, and crawlable, metadata-rich pages.

## Commands

```bash
# Setup
uv sync

# Run app locally
python app.py

# Verify runtime deps
python -c "import flask; import holidays; print('ok')"

# Frontend template best-practice checks
uv run python .github/agentic/skills/frontend/ui-implementation-standards/scripts/check_ui_templates.py

# SEO template best-practice checks
uv run python .github/agentic/skills/seo/technical-seo-checklist/scripts/check_seo_templates.py
```

## Architecture

### Backend

- `app.py` defines all Flask routes and holiday data transformations.
- Main rendered routes:
  - `GET /`
  - `GET /mentions-legales`
  - `GET /privacy-policy`
- API routes:
  - `GET /api/countries`
  - `GET /api/subdivisions/<country_code>`
  - `GET /api/holidays/<country_code>/<year>?subdiv=<code>`
  - `GET /api/school-holidays/FR/<year>?zone=A|B|C`

### Frontend

- Primary UI is in `templates/index.html`.
- Uses CDN assets for Bootstrap and FullCalendar.
- Frontend JS in the template fetches API data and updates calendar events.

## Frontend conventions

- Keep UI changes responsive across mobile and desktop breakpoints.
- Prefer semantic HTML (`header`, `main`, `nav`, `footer`) when restructuring.
- Preserve accessibility basics:
  - meaningful labels and button text
  - keyboard-friendly interactions
  - sufficient color contrast for key states
- Keep JavaScript modular and explicit; avoid duplicating request logic.
- For API-driven UI updates, handle failed responses explicitly and keep the UI
  in a safe state.
- Preserve existing behavior for country, subdivision, zone, and year selectors
  unless the request explicitly changes it.

### Frontend best practices

- Prefer progressive enhancement so key content remains understandable before JS.
- Keep event handling deterministic and avoid duplicate listeners.
- Keep UI state transitions explicit for loading, success, and error states.
- Favor class-based styling over inline style growth for maintainability.
- Validate template-level a11y and structure using:
  - `.github/agentic/skills/frontend/ui-implementation-standards/scripts/check_ui_templates.py`

## Technical SEO conventions

- Every user-facing rendered page should have:
  - a unique, descriptive `<title>`
  - a meaningful `meta name="description"`
  - a canonical URL tag when relevant
- Use clear heading hierarchy (`h1` then logical `h2`/`h3` levels).
- Keep important content server-rendered in templates (not JS-only).
- Ensure links are crawlable anchor tags with valid `href`.
- When adding new public pages, update internal linking (for example footer or
  nav) so pages are discoverable.
- Avoid duplicate metadata and placeholder SEO content in production-ready pages.
- Favor performance-safe changes:
  - avoid blocking scripts when possible
  - avoid unnecessary large assets
  - keep render path simple

### Technical SEO best practices

- Keep title and meta description unique for each user-facing template.
- Ensure each page has one clear `<h1>` and logical subheadings.
- Avoid placeholder or boilerplate metadata in shipping pages.
- Keep internal links crawlable and stable.
- Validate template SEO fields using:
  - `.github/agentic/skills/seo/technical-seo-checklist/scripts/check_seo_templates.py`

## Agentic skills process

Local skills live under `.github/agentic/skills/**`.

### Skills-first enforcement (mandatory, all skills)
- For any request covered by a local skill in `.github/agentic/skills/**`,
  follow the skill workflow first, before using direct MCP, terminal, or ad-hoc
  actions.
- If runtime skill discovery does not expose the skill, load its local
  `SKILL.md` manually and apply its **Required Behavior**, **Workflow**, and
  **Review Checks** sections.
- If a skill script/tool dependency is missing (for example `uv`), stop and ask
  the user for fallback approval; do not skip directly to ad-hoc drafting.
- In final responses for skill-driven tasks, state whether execution was via
  runtime skill loading or local `SKILL.md` fallback.

### Frontend implementation standards
- Use the skill at
  `.github/agentic/skills/frontend/ui-implementation-standards/SKILL.md` for
  frontend/UI tasks.
- **Mandatory trigger**: when a request changes templates, UI behavior,
  responsiveness, accessibility, or client-side rendering logic.
- Follow the skill before broad refactors or ad-hoc HTML/CSS/JS rewrites.

### Technical SEO checklist
- Use the skill at
  `.github/agentic/skills/seo/technical-seo-checklist/SKILL.md` for SEO tasks.
- **Mandatory trigger**: when a request affects page metadata, crawlability,
  content structure, indexability, or discoverability.
- Apply the checklist before shipping SEO-impacting template changes.

### Pull request authoring workflow
- Use the live skill at
  `.github/agentic/skills/github/pull-request-authoring-workflow/SKILL.md` for
  pull request work.
- **Mandatory trigger**: when the user asks to open/create/update a PR (or asks
  PR title/body/help), load and follow `pull-request-authoring-workflow` before
  using direct GitHub MCP PR actions.
- Draft PR titles and bodies locally from the branch, diff, and
  `.github/pull_request_template.md`.
- Use
  `.github/agentic/skills/github/pull-request-authoring-workflow/scripts/draft_pr.py`
  to bootstrap PR drafts.
- Use the GitHub MCP only for GitHub-side PR actions such as creating or
  updating the pull request.
- Keep checklist items unchecked, link related tickets, and never include
  secrets or hardcoded credentials.
- Before creating a PR, check whether an open PR already exists for the current
  head branch and update it instead of creating a duplicate.
- Never call GitHub MCP PR write actions until title/body are drafted from the
  skill process (script or approved fallback).
- If the skill or its scripts are unavailable, stop and ask the user how to
  proceed; do not silently bypass the process.

### Commit message guidelines
- Use the live skill at
  `.github/agentic/skills/github/commit-message-guidelines/SKILL.md` for commit
  message work.
- **Mandatory trigger**: when the user asks to write/suggest/fix a commit
  message, load and follow `commit-message-guidelines` before drafting.
- Review `git diff --staged` before drafting the message.
- Draft commit messages locally and use
  `.github/agentic/skills/github/commit-message-guidelines/scripts/suggest_commit_message.py`
  to bootstrap them.
- Use the conventional commit format `<type>(<scope>): <description>` with an
  imperative summary.
- Use the GitHub MCP only for GitHub-side repository actions, not for plain
  commit-message drafting.
- Base the message only on staged changes; do not infer scope from
  unstaged/untracked files.
- If nothing is staged, stop and ask the user whether to stage changes first; do
  not guess a message.
- Never draft a commit message before reviewing `git diff --staged` and applying
  the skill's type/scope rules.
- If the skill or its scripts are unavailable, stop and ask the user how to
  proceed; do not silently bypass the process.

## Quality checks before final answer

- Confirm changed routes/templates still map correctly to user-visible pages.
- Confirm new frontend behavior is responsive and accessible by design.
- Confirm SEO-critical fields (`title`, meta description, heading hierarchy,
  canonical usage) are present for any changed page templates.
- Keep guidance and examples aligned with actual repository files and commands.
