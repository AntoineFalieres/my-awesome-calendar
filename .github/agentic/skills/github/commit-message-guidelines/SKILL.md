---
name: commit-message-guidelines
description: Prepare commit messages for this repo using the required conventional commit rules. Use when reviewing staged changes, choosing a commit type, selecting a scope, writing a commit summary, or checking whether a commit message follows the repository format.
---

# Commit Message Guidelines

Use this skill when preparing or reviewing a commit message for this repository.

## Quick Start

Review the staged diff before writing the commit message:

```bash
git diff --staged
```

Generate a suggested conventional commit message from the staged diff:

```bash
uv run python \
	.github/agentic/skills/github/commit-message-guidelines/scripts/suggest_commit_message.py
```

Override the inferred type, scope, or summary when needed:

```bash
uv run python \
	.github/agentic/skills/github/commit-message-guidelines/scripts/suggest_commit_message.py \
	--type docs \
	--scope agentic \
	--summary "add commit message helper"
```

## Required Behavior

- Review staged changes before drafting the commit message.
- Draft commit messages locally from `git diff --staged`.
- Use `scripts/suggest_commit_message.py` to bootstrap drafts from this skill folder.
- Use GitHub MCP only for GitHub-side repository actions.
- Follow the repository conventional commit format.
- Choose the message type based on the actual change, not the file name alone.
- Keep the summary concise and written in imperative mood.
- Use a scope when it adds useful context about the affected area.

## Commit Message Format

Commit messages should use this format:

```text
<type>(<scope>): <description>
```

Example:

```text
feat(stock): add new stock model for OBT
```

The scope is optional when it does not improve clarity.

## Allowed Types

- `feat`: a new feature
- `fix`: a bug fix
- `refactor`: a code change that neither fixes a bug nor adds a feature
- `test`: adding missing tests or correcting existing tests
- `docs`: documentation changes
- `chore`: changes to build process or auxiliary tools and libraries such as documentation generation
- `style`: changes that do not affect the meaning of the code
- `ci`: changes to CI configuration or workflows
- `perf`: a code change that improves performance
- `build`: changes that affect the build system or external dependencies
- `revert`: reverts a previous commit

## Workflow

1. Run `git diff --staged` to inspect exactly what will be committed.
2. Determine the dominant intent of the staged change.
3. Choose the matching conventional commit type.
4. Add a scope if it clarifies the affected area, domain, or subsystem.
5. Write a short imperative description that matches the staged diff.
6. Recheck that the message is specific, accurate, and not broader than the staged change.

## Review Checks

Before finalizing the commit message, confirm:

- The message matches the `<type>(<scope>): <description>` format when a scope is used.
- The selected type matches the staged change.
- The summary is imperative, concise, and specific.
- The scope, if present, adds real context rather than noise.
- The message reflects the staged diff instead of unstaged or intended follow-up work.

## Notes

- Prefer evidence from the staged diff over assumptions about what the change was meant to do.
- If multiple unrelated changes are staged, split them before committing rather than forcing one vague commit message.
- Typical scopes in this repository can be domains such as `stock`, `sales`, `docs`, `ci`, or another affected subsystem.
- Do not route plain commit-message drafting through GitHub MCP.