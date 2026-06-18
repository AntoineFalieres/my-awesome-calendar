---
description: Create or update a pull request for this repository using the PR authoring workflow skill.
tools: ['changes', 'githubRepo', 'github/github-mcp-server/pull_request_read', 'github/github-mcp-server/pull_request_write']
---

## User Input

```text
$ARGUMENTS
```

You MUST consider the user input before proceeding (if not empty).

## Goal

Create or update a pull request using the repository PR authoring workflow skill at
`.github/agentic/skills/github/pull-request-authoring-workflow/SKILL.md`.

## Required Workflow

1. Read and follow the skill at `.github/agentic/skills/github/pull-request-authoring-workflow/SKILL.md`.
1. Extract any ticket ID from the current branch name (format: `CDM-123` or similar).
1. Review the branch diff to determine the correct conventional commit type and imperative summary.
1. Build the PR title: `<type>(<ticket-id>): <imperative summary>` — omit ticket when absent.
1. Draft the PR body from `.github/pull_request_template.md`, filling in:
   - PR type checkboxes (check only the applicable ones)
   - Description
   - Breaking changes (`No breaking changes` unless schema shape changes)
   - Changes made list
   - Related issues / tickets
1. Leave all checklist items unchecked.
1. Create or update the PR via GitHub MCP.
1. Confirm the PR URL after creation or update.
