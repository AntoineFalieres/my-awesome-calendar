from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
PR_TEMPLATE_PATH = REPO_ROOT / ".github" / "pull_request_template.md"
TICKET_ID_PATTERN = re.compile(r"[A-Z][A-Z0-9]+-\d+")


def run_git_command(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def get_branch_name() -> str:
    return run_git_command("rev-parse", "--abbrev-ref", "HEAD")


def extract_ticket_id(branch_name: str) -> str | None:
    match = TICKET_ID_PATTERN.search(branch_name)
    if match is None:
        return None
    return match.group(0)


def get_changed_files() -> list[str]:
    staged = run_git_command("diff", "--cached", "--name-only").splitlines()
    unstaged = run_git_command("diff", "--name-only").splitlines()
    seen: set[str] = set()
    changed_files: list[str] = []

    for path in staged + unstaged:
        normalized_path = path.strip()
        if not normalized_path or normalized_path in seen:
            continue
        seen.add(normalized_path)
        changed_files.append(normalized_path)

    return changed_files


def infer_change_type(changed_files: list[str]) -> str:
    if not changed_files:
        return "chore"

    if all(path.startswith("docs/") or path.endswith(".md") for path in changed_files):
        return "docs"

    if all(path.startswith("tests/") or "test" in Path(path).parts for path in changed_files):
        return "test"

    if any(path.startswith(".github/workflows/") for path in changed_files):
        return "ci"

    if any(Path(path).name in {"packages.yml", "package-lock.yml", "requirements.txt", "pyproject.toml"} for path in changed_files):
        return "build"

    if any(path.startswith(".github/") for path in changed_files):
        return "chore"

    return "feat"


def summarize_scope(changed_files: list[str]) -> str:
    if not changed_files:
        return "repo"

    first_path = Path(changed_files[0])
    for part in first_path.parts:
        if part not in {"models", "macros", "tests", ".github", "docs"}:
            return part.replace("_", "-")

    return first_path.stem.replace("_", "-")


def build_title(change_type: str, ticket_id: str | None, summary: str, scope: str) -> str:
    normalized_summary = summary.strip()
    if ticket_id:
        return f"{change_type}({ticket_id}): {normalized_summary}"
    return f"{change_type}({scope}): {normalized_summary}"


def build_changes_made(changed_files: list[str]) -> str:
    if not changed_files:
        return "- Review the current branch changes and replace this placeholder with the actual implementation summary."

    bullets = [f"- Update `{path}`" for path in changed_files[:10]]
    if len(changed_files) > 10:
        bullets.append(f"- Update {len(changed_files) - 10} additional files")
    return "\n".join(bullets)


def build_description(change_type: str, branch_name: str, summary: str) -> str:
    return (
        f"This PR introduces a {change_type} change from branch `{branch_name}`. "
        f"It focuses on {summary}."
    )


def render_body(template: str, description: str, breaking_changes: str, changes_made: str, related_issue: str) -> str:
    replacements = {
        "[Provide a brief description of what this PR achieves. Explain the problem it solves or the feature it adds.]": description,
        "[Fill this section only when the PR impacts a column schema: column removal, column creation, column addition, or column type change. Otherwise leave `No breaking changes`.]": breaking_changes,
        "[List the specific changes you've made in this PR. Be detailed, especially if your PR includes multiple changes.]": f"{changes_made}\n\nRelated issue: {related_issue}",
    }

    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Draft a pull request title and body from the current branch and git diff."
    )
    parser.add_argument(
        "--summary",
        help="Imperative summary to use in the PR title and description.",
        default="summarize the current branch changes",
    )
    parser.add_argument(
        "--type",
        dest="change_type",
        help="Override the inferred conventional commit type.",
    )
    parser.add_argument(
        "--breaking-changes",
        default="No breaking changes",
        help="Breaking changes text for the PR template.",
    )
    parser.add_argument(
        "--related-issue",
        default="Add ticket link here",
        help="Ticket or issue reference to place in the PR body.",
    )
    parser.add_argument(
        "--output",
        help="Optional path for the rendered PR body file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not PR_TEMPLATE_PATH.exists():
        print(f"PR template not found: {PR_TEMPLATE_PATH}", file=sys.stderr)
        return 1

    try:
        branch_name = get_branch_name()
        ticket_id = extract_ticket_id(branch_name)
        changed_files = get_changed_files()
    except subprocess.CalledProcessError as error:
        print(error.stderr.strip(), file=sys.stderr)
        return 1

    change_type = args.change_type or infer_change_type(changed_files)
    scope = summarize_scope(changed_files)
    title = build_title(change_type, ticket_id, args.summary, scope)
    template = PR_TEMPLATE_PATH.read_text()
    body = render_body(
        template=template,
        description=build_description(change_type, branch_name, args.summary),
        breaking_changes=args.breaking_changes,
        changes_made=build_changes_made(changed_files),
        related_issue=args.related_issue,
    )

    print("Suggested title:")
    print(title)
    print()
    print("Suggested body:")
    print(body)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = REPO_ROOT / output_path
        output_path.write_text(body)
        print()
        print(f"Wrote PR body to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())