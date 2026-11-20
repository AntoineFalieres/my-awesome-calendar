---
name: pull-request-authoring-workflow
description: Create or update pull requests for this repo using the required process. Use when opening a PR, editing a PR body, preparing a PR title, checking the pull request template, applying conventional commit style to PR titles, or verifying GitHub PR rendering.
---

# Pull Request Authoring Workflow

Use this skill when preparing, creating, or updating a pull request for this repository.

## Quick Start

Generate a suggested title and body from the current branch and diff:

```bash
uv run python .github/skills/github/pull-request-authoring-workflow/scripts/draft_pr.py \
	--summary "add an imperative summary here"
```

Write the rendered body to a file for GitHub MCP review or CLI fallback:

```bash
uv run python .github/skills/github/pull-request-authoring-workflow/scripts/draft_pr.py \
	--summary "add an imperative summary here" \
	--output pr_body.md
```

## Required Behavior

- Draft PR titles and bodies locally from the branch, diff, and template.
- Use `scripts/draft_pr.py` to bootstrap drafts from this skill folder.
- Use GitHub MCP only for GitHub-side PR actions.
- Use the repository template at `.github/pull_request_template.md` as the starting point for the PR body.
- Keep the checklist visible, but do not pre-check any checklist items.
- Include a clear PR description and an explicit list of changes.
- The draft generator includes staged and unstaged tracked files only. Untracked files are excluded from its generated change list; add relevant untracked files manually before publishing.
- Do not include secrets, credentials, or hardcoded sensitive values.

## PR Title Rules

PR titles must follow the repository convention:

```text
<type>(<scope>): <imperative summary>
```

Example:

```text
feat(agentic): automate roadmap todo changelog updates
```

Rules:

- Use a conventional commit type such as `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `ci`, `perf`, `build`, or `revert`.
- Write the summary in imperative mood.
- Keep the title concise and specific to the actual change.

## PR Body Rules

- Start from `.github/pull_request_template.md`.
- Preserve markdown structure so headings, bullets, and checklists render correctly.
- When a body is built outside MCP and must be passed through the GitHub CLI, use a file-based payload such as `gh pr create --body-file <file>.md` or `gh pr edit --body-file <file>.md`.
- Never pass escaped newline sequences inline for multi-line PR bodies.
- Keep the breaking changes section as `No breaking changes` unless the PR changes schema shape or column types.

## Workflow

1. Inspect the current branch name.
2. Review the staged or working-tree changes to determine the correct conventional commit type and concise summary.
3. Build the PR title from the change type, scope, and imperative summary.
4. Draft the PR body from `.github/pull_request_template.md`.
5. Fill in the description, breaking changes section, and changes made section with repository-specific details.
6. Leave checklist items unchecked.
7. Create or update the PR with GitHub MCP.
8. After creation or update, reload the PR and verify the title, rendered description, breaking changes and changes made sections, and unchecked checklist items. Correct any mismatch and verify again.

## Review Checks

Before finalizing the PR, confirm:

- The title matches the required conventional format.
- The template sections are preserved.
- Checklist boxes remain unchecked.
- The rendered markdown displays headings, bullets, and checklist items on separate lines.

## Notes

- Prefer repository evidence over guesswork when summarizing changes.
- If the user asks to create a PR, gather the missing title/body details from the branch, diff, and template before opening it.
- Do not route plain PR title or body drafting through GitHub MCP.