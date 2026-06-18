from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
DEPENDENCY_FILES = {
    "packages.yml",
    "package-lock.yml",
    "requirements.txt",
    "pyproject.toml",
}


def run_git_command(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def get_staged_files() -> list[str]:
    return [
        path.strip()
        for path in run_git_command("diff", "--staged", "--name-only").splitlines()
        if path.strip()
    ]


def infer_commit_type(staged_files: list[str]) -> str:
    if not staged_files:
        return "chore"

    if all(path.startswith("docs/") or path.endswith(".md") for path in staged_files):
        return "docs"

    if all(path.startswith("tests/") or "test" in Path(path).parts for path in staged_files):
        return "test"

    if any(path.startswith(".github/workflows/") for path in staged_files):
        return "ci"

    if any(Path(path).name in DEPENDENCY_FILES for path in staged_files):
        return "build"

    if any(path.startswith(".github/") for path in staged_files):
        return "chore"

    return "feat"


def infer_scope(staged_files: list[str]) -> str:
    if not staged_files:
        return "repo"

    first_path = Path(staged_files[0])
    ignored_parts = {"models", "macros", "tests", ".github", "docs", "scripts"}

    for part in first_path.parts:
        if part not in ignored_parts:
            return part.replace("_", "-")

    return first_path.stem.replace("_", "-")


def build_message(commit_type: str, scope: str | None, summary: str) -> str:
    normalized_summary = summary.strip()
    if scope:
        return f"{commit_type}({scope}): {normalized_summary}"
    return f"{commit_type}: {normalized_summary}"


def build_summary(staged_files: list[str], scope: str, commit_type: str) -> str:
    if not staged_files:
        return "review staged changes and update this message"

    if commit_type == "docs":
        return f"update {scope} documentation"

    if commit_type == "test":
        return f"add tests for {scope}"

    if commit_type == "ci":
        return f"update {scope} workflow"

    if commit_type == "build":
        return f"update {scope} dependencies"

    if commit_type == "chore":
        return f"update {scope} tooling"

    return f"update {scope} logic"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Suggest a conventional commit message from the staged git diff."
    )
    parser.add_argument(
        "--type",
        dest="commit_type",
        help="Override the inferred conventional commit type.",
    )
    parser.add_argument(
        "--scope",
        help="Override the inferred commit scope. Pass an empty string to omit the scope.",
    )
    parser.add_argument(
        "--summary",
        help="Override the inferred imperative summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        staged_files = get_staged_files()
    except subprocess.CalledProcessError as error:
        print(error.stderr.strip(), file=sys.stderr)
        return 1

    if not staged_files:
        print(
            "No staged files detected. Stage changes first, then run this command.",
            file=sys.stderr,
        )
        return 1

    commit_type = args.commit_type or infer_commit_type(staged_files)

    if args.scope == "":
        scope = None
    else:
        scope = args.scope or infer_scope(staged_files)

    summary = args.summary or build_summary(staged_files, scope or "repo", commit_type)
    message = build_message(commit_type, scope, summary)

    print("Suggested commit message:")
    print(message)
    print()
    print("Staged files:")
    for path in staged_files:
        print(f"- {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())