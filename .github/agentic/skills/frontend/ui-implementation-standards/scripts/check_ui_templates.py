from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
DEFAULT_TEMPLATE_GLOB = "templates/*.html"

TAG_PATTERN = re.compile(r"<(input|select|textarea|button)\b([^>]*)>", re.IGNORECASE)
IMG_PATTERN = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"<h([1-6])\b", re.IGNORECASE)


def has_attr(attrs: str, name: str) -> bool:
    return re.search(rf'\b{name}\s*=\s*["\'][^"\']+["\']', attrs, re.IGNORECASE) is not None


def get_attr_value(attrs: str, name: str) -> str | None:
    match = re.search(rf'\b{name}\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
    if match is None:
        return None
    return match.group(1).strip()


def gather_templates(template_glob: str) -> list[Path]:
    return sorted(REPO_ROOT.glob(template_glob))


def check_heading_order(html: str) -> list[str]:
    levels = [int(level) for level in HEADING_PATTERN.findall(html)]
    issues: list[str] = []
    if not levels:
        return issues

    if levels[0] != 1:
        issues.append("Heading sequence should start with <h1>.")

    previous = levels[0]
    for level in levels[1:]:
        if level - previous > 1:
            issues.append(f"Heading jump detected: <h{previous}> to <h{level}>.")
        previous = level

    return issues


def check_controls(html: str) -> list[str]:
    issues: list[str] = []
    label_targets = set(
        re.findall(r'<label[^>]*\bfor\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    )

    for tag_name, attrs in TAG_PATTERN.findall(html):
        lower_tag = tag_name.lower()
        has_aria_label = has_attr(attrs, "aria-label") or has_attr(attrs, "aria-labelledby")
        control_id = get_attr_value(attrs, "id")
        has_label = control_id in label_targets if control_id else False

        if lower_tag == "input":
            input_type = (get_attr_value(attrs, "type") or "text").lower()
            if input_type in {"hidden", "submit", "button"}:
                continue

        if not has_aria_label and not has_label:
            issues.append(f"<{lower_tag}> is missing aria-label/aria-labelledby or a <label for=...>.")

    return issues


def check_images(html: str) -> list[str]:
    issues: list[str] = []
    for attrs in IMG_PATTERN.findall(html):
        if not has_attr(attrs, "alt"):
            issues.append("<img> is missing an alt attribute.")
    return issues


def check_template(path: Path) -> tuple[list[str], list[str]]:
    html = path.read_text(encoding="utf-8")
    issues: list[str] = []
    warnings: list[str] = []

    if re.search(r'<meta[^>]*\bname\s*=\s*["\']viewport["\']', html, re.IGNORECASE) is None:
        issues.append("Missing viewport meta tag.")

    if re.search(r"<main\b", html, re.IGNORECASE) is None:
        warnings.append("No <main> landmark found.")

    issues.extend(check_heading_order(html))
    issues.extend(check_controls(html))
    issues.extend(check_images(html))

    return issues, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run lightweight UI/a11y checks against HTML templates."
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
