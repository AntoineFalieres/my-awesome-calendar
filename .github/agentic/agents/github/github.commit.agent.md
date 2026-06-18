---
description: Draft a conventional commit message for staged changes using the repository commit message guidelines skill.
tools: ['changes']
---

## User Input

```text
$ARGUMENTS
```

You MUST consider the user input before proceeding (if not empty).

## Goal

Draft a commit message using the repository commit message guidelines skill at
`.github/agentic/skills/github/commit-message-guidelines/SKILL.md`.

## Required Workflow

1. Read and follow the skill at `.github/agentic/skills/github/commit-message-guidelines/SKILL.md`.
1. Run `git diff --staged` to inspect exactly what will be committed.
1. Determine the dominant intent of the staged change.
1. Choose the matching conventional commit type.
1. Add a scope if it clarifies the affected area, domain, or subsystem.
1. Write a short imperative description that matches the staged diff.
1. Return one primary recommended message.

## Output Contract

- Primary message: `<type>(<scope>): <description>`
- Do not commit — only draft the message unless the user explicitly asks to commit.
