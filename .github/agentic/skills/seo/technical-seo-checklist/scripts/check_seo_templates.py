from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
DEFAULT_TEMPLATE_GLOB = "templates/*.html"
PLACEHOLDER_PHRASES = {"to be completed", "placeholder", "todo", "lorem ipsum"}


def gather_templates(template_glob: str) -> list[Path]:
    return sorted(REPO_ROOT.glob(template_glob))


def find_title(html: str) -> str | None:
    match = re.search(r"<title>\s*(.*?)\s*</title>", html, re.IGNORECASE | re.DOTALL)
    if match is None:
        return None
    return re.sub(r"\s+", " ", match.group(1)).strip()


def find_meta_description(html: str) -> str | None:
    pattern = re.compile(
        r'<meta[^>]*\bname\s*=\s*["\']description["\'][^>]*\bcontent\s*=\s*["\']([^"\']*)["\']',
        re.IGNORECASE,
    )
    match = pattern.search(html)
    if match is None:
        return None
    return re.sub(r"\s+", " ", match.group(1)).strip()


def find_lang(html: str) -> str | None:
    match = re.search(r'<html[^>]*\blang\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    if match is None:
        return None
    return match.group(1).strip()


def check_template(path: Path) -> tuple[list[str], list[str]]:
    html = path.read_text(encoding="utf-8")
    issues: list[str] = []
    warnings: list[str] = []

    title = find_title(html)
    if not title:
        issues.append("Missing <title> tag.")
    else:
        lowered = title.lower()
        if any(phrase in lowered for phrase in PLACEHOLDER_PHRASES):
            issues.append("Title appears to contain placeholder text.")
        if len(title) < 20 or len(title) > 70:
            warnings.append("Title length is outside recommended range (20-70 chars).")

    description = find_meta_description(html)
    if not description:
        issues.append("Missing meta description.")
    else:
        lowered = description.lower()
        if any(phrase in lowered for phrase in PLACEHOLDER_PHRASES):
            issues.append("Meta description appears to contain placeholder text.")
        if len(description) < 70 or len(description) > 160:
            warnings.append(
                "Meta description length is outside recommended range (70-160 chars)."
            )

    h1_count = len(re.findall(r"<h1\b", html, re.IGNORECASE))
    if h1_count == 0:
        issues.append("Missing <h1>.")
    elif h1_count > 1:
        warnings.append("Multiple <h1> tags found.")

    lang = find_lang(html)
    if not lang:
        issues.append("Missing language attribute on <html>.")

    canonical_match = re.search(
        r'<link[^>]*\brel\s*=\s*["\']canonical["\'][^>]*\bhref\s*=\s*["\']([^"\']*)["\']',
        html,
        re.IGNORECASE,
    )
    if canonical_match and not canonical_match.group(1).strip():
        issues.append("Canonical link exists but href is empty.")

    return issues, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run lightweight technical SEO checks against HTML templates."
    )
    parser.add_argument(
        "--templates",
        default=DEFAULT_TEMPLATE_GLOB,
        help=f"Glob pattern relative to repo root (default: {DEFAULT_TEMPLATE_GLOB}).",
    )
    parser.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Exit with code 1 when issues are found.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    template_paths = gather_templates(args.templates)
    if not template_paths:
        print(f"No templates matched: {args.templates}", file=sys.stderr)
        return 1

    total_issues = 0
    total_warnings = 0

    for template_path in template_paths:
        issues, warnings = check_template(template_path)
        relative_path = template_path.relative_to(REPO_ROOT)
        print(f"Template: {relative_path}")

        if not issues and not warnings:
            print("  OK")
            continue

        for issue in issues:
            print(f"  ISSUE: {issue}")
        for warning in warnings:
            print(f"  WARN: {warning}")

        total_issues += len(issues)
        total_warnings += len(warnings)

    print()
    print(f"Summary: {total_issues} issue(s), {total_warnings} warning(s)")

    if args.fail_on_issues and total_issues > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
