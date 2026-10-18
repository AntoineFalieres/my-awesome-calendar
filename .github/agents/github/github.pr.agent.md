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
`.github/skills/github/pull-request-authoring-workflow/SKILL.md`.

## Required Workflow

1. Read and follow the skill at `.github/skills/github/pull-request-authoring-workflow/SKILL.md`.
2. Review the branch diff to determine the correct conventional commit type and imperative summary.
3. Build the PR title: `<type>(<scope>): <imperative summary>` — omit scope when absent.
4. Draft the PR body from `.github/pull_request_template.md`, filling in:
   - PR type checkboxes (check only the applicable ones)
   - Description
   - Breaking changes (`No breaking changes` unless schema shape changes)
   - Changes made list
   - Related issues / tickets
5. Leave all checklist items unchecked.
6. Create or update the PR via GitHub MCP.
7. Confirm the PR URL after creation or update.
