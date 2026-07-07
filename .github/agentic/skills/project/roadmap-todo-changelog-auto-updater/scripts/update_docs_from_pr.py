from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
ROADMAP_PATH = REPO_ROOT / "ROADMAP.md"
TODO_PATH = REPO_ROOT / "TODO.md"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"

ROLE_ORDER = ["PM", "SEO", "UX/UI", "Full-Stack", "Ad Ops"]

ROADMAP_MARKERS = (
    "<!-- AUTO-ROADMAP-UPDATES:START -->",
    "<!-- AUTO-ROADMAP-UPDATES:END -->",
)
TODO_MARKERS = (
    "<!-- AUTO-TODO-UPDATES:START -->",
    "<!-- AUTO-TODO-UPDATES:END -->",
)
CHANGELOG_MARKERS = (
    "<!-- AUTO-CHANGELOG-UPDATES:START -->",
    "<!-- AUTO-CHANGELOG-UPDATES:END -->",
)


@dataclass(frozen=True)
class PullRequestMetadata:
    number: int
    title: str
    body: str
    url: str
    merged_date: str
    changed_files: list[str]


ROLE_RULES = {
    "PM": {
        "path_keywords": [],
        "text_keywords": [
            "roadmap",
            "scope",
            "priority",
            "mvp",
            "strategy",
            "product",
            "acceptance criteria",
        ],
        "todo_template": "review scope and roadmap impact from merged PR #{number}.",
    },
    "SEO": {
        "path_keywords": ["sitemap", "robots", "seo", "canonical", "schema", "json-ld"],
        "text_keywords": ["seo", "meta", "canonical", "schema", "json-ld", "crawl", "index"],
        "todo_template": "review metadata/indexability implications from merged PR #{number}.",
    },
    "UX/UI": {
        "path_keywords": ["templates/", "static/", ".css", ".js"],
        "text_keywords": ["ui", "ux", "responsive", "accessibility", "layout", "footer"],
        "todo_template": "review readability and interaction impact from merged PR #{number}.",
    },
    "Full-Stack": {
        "path_keywords": ["app.py", "api/", ".py", "requirements.txt", "pyproject.toml"],
        "text_keywords": ["backend", "api", "flask", "route", "integration"],
        "todo_template": "validate implementation consistency from merged PR #{number}.",
    },
    "Ad Ops": {
        "path_keywords": ["ads.txt", "adsense", "monetization", "consent", "cookie", "gdpr"],
        "text_keywords": ["adsense", "ad ops", "monetization", "gdpr", "consent", "cookie"],
        "todo_template": "review monetization/compliance implications from merged PR #{number}.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update ROADMAP.md, TODO.md, and CHANGELOG.md from merged PR metadata."
    )
    parser.add_argument(
        "--pr-json",
        required=True,
        help="Path to a JSON file containing merged PR metadata.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print summary without writing files.",
    )
    return parser.parse_args()


def read_pr_metadata(pr_json_path: Path) -> PullRequestMetadata:
    payload = json.loads(pr_json_path.read_text(encoding="utf-8"))

    files: list[str] = []
    for entry in payload.get("files", []):
        if isinstance(entry, str):
            files.append(entry)
            continue
        if isinstance(entry, dict):
            path = entry.get("filename") or entry.get("path")
            if isinstance(path, str) and path:
                files.append(path)

    merged_at = str(payload.get("merged_at", "")).strip()
    merged_date = merged_at[:10] if len(merged_at) >= 10 else "unknown-date"

    return PullRequestMetadata(
        number=int(payload["number"]),
        title=str(payload.get("title", "")).strip(),
        body=str(payload.get("body", "")).strip(),
        url=str(payload.get("html_url", "")).strip(),
        merged_date=merged_date,
        changed_files=sorted(set(files)),
    )


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def infer_roles(metadata: PullRequestMetadata) -> list[str]:
    matched_roles: list[str] = []
    files_blob = "\n".join(path.lower() for path in metadata.changed_files)
    text_blob = f"{metadata.title}\n{metadata.body}".lower()

    for role in ROLE_ORDER:
        rule = ROLE_RULES[role]
        if contains_any(files_blob, rule["path_keywords"]) or contains_any(
            text_blob, rule["text_keywords"]
        ):
            matched_roles.append(role)

    if not matched_roles:
        return ["Full-Stack"]
    return matched_roles


def ensure_managed_section(
    content: str,
    section_title: str,
    start_marker: str,
    end_marker: str,
    preface: str,
) -> str:
    if start_marker in content and end_marker in content:
        return content

    trimmed = content.rstrip()
    if trimmed:
        trimmed += "\n\n"
    trimmed += (
        f"## {section_title}\n\n"
        f"{start_marker}\n"
        f"{preface}\n"
        f"{end_marker}\n"
    )
    return trimmed


def inject_entry_after_heading(
    block_content: str,
    heading_line: str,
    entry_lines: list[str],
    token: str,
) -> tuple[str, bool]:
    if token in block_content:
        return block_content, False

    rendered_entry = "\n".join(entry_lines).rstrip()
    if not block_content.strip():
        return f"{heading_line}\n\n{rendered_entry}\n", True

    if heading_line in block_content:
        _, suffix = block_content.split(heading_line, 1)
        suffix = suffix.lstrip("\n")
        new_content = f"{heading_line}\n\n{rendered_entry}\n"
        if suffix:
            new_content += f"\n{suffix.rstrip()}\n"
        return new_content, True

    return rendered_entry + "\n\n" + block_content.lstrip("\n"), True


def upsert_block(content: str, start_marker: str, end_marker: str, new_block: str) -> str:
    start_index = content.index(start_marker) + len(start_marker)
    end_index = content.index(end_marker, start_index)
    return content[:start_index] + "\n" + new_block.rstrip() + "\n" + content[end_index:]


def update_roadmap(content: str, metadata: PullRequestMetadata, roles: list[str]) -> tuple[str, bool]:
    start_marker, end_marker = ROADMAP_MARKERS
    updated = ensure_managed_section(
        content=content,
        section_title="Auto-managed updates",
        start_marker=start_marker,
        end_marker=end_marker,
        preface="### Next from merged PRs",
    )
    start_index = updated.index(start_marker) + len(start_marker)
    end_index = updated.index(end_marker, start_index)
    block = updated[start_index:end_index].strip("\n")

    token = f"<!-- AUTO-PR:{metadata.number} -->"
    line = (
        f"- {metadata.merged_date} - PR #{metadata.number} `{metadata.title}` "
        f"- Roles: {', '.join(roles)} ({metadata.url}) {token}"
    )
    new_block, changed = inject_entry_after_heading(
        block_content=block,
        heading_line="### Next from merged PRs",
        entry_lines=[line],
        token=token,
    )
    return upsert_block(updated, start_marker, end_marker, new_block), changed


def update_todo(content: str, metadata: PullRequestMetadata, roles: list[str]) -> tuple[str, bool]:
    start_marker, end_marker = TODO_MARKERS
    updated = ensure_managed_section(
        content=content,
        section_title="Auto-managed updates",
        start_marker=start_marker,
        end_marker=end_marker,
        preface="### Role-owned follow-ups from merged PRs",
    )
    start_index = updated.index(start_marker) + len(start_marker)
    end_index = updated.index(end_marker, start_index)
    block = updated[start_index:end_index].strip("\n")

    block_out = block
    changed_any = False
    if not block_out.strip():
        block_out = "### Role-owned follow-ups from merged PRs\n"

    for role in roles:
        token = f"<!-- AUTO-PR:{metadata.number};ROLE:{role} -->"
        if token in block_out:
            continue
        todo_text = ROLE_RULES[role]["todo_template"].format(number=metadata.number)
        line = f"- [ ] **{role}:** {todo_text} {token}"
        block_out = block_out.rstrip() + "\n" + line + "\n"
        changed_any = True

    return upsert_block(updated, start_marker, end_marker, block_out), changed_any


def update_changelog(content: str, metadata: PullRequestMetadata, roles: list[str]) -> tuple[str, bool]:
    seed = content.rstrip()
    if not seed:
        seed = "# CHANGELOG\n"

    start_marker, end_marker = CHANGELOG_MARKERS
    updated = ensure_managed_section(
        content=seed,
        section_title="Auto-managed updates",
        start_marker=start_marker,
        end_marker=end_marker,
        preface="### Merged PR entries",
    )
    start_index = updated.index(start_marker) + len(start_marker)
    end_index = updated.index(end_marker, start_index)
    block = updated[start_index:end_index].strip("\n")

    token = f"<!-- AUTO-PR:{metadata.number} -->"
    line = (
        f"- {metadata.merged_date} - PR #{metadata.number}: {metadata.title} "
        f"(Roles: {', '.join(roles)}) {metadata.url} {token}"
    )
    new_block, changed = inject_entry_after_heading(
        block_content=block,
        heading_line="### Merged PR entries",
        entry_lines=[line],
        token=token,
    )
    return upsert_block(updated, start_marker, end_marker, new_block), changed


def main() -> int:
    args = parse_args()
    metadata = read_pr_metadata(Path(args.pr_json))
    roles = infer_roles(metadata)

    roadmap_before = ROADMAP_PATH.read_text(encoding="utf-8")
    todo_before = TODO_PATH.read_text(encoding="utf-8")
    changelog_before = CHANGELOG_PATH.read_text(encoding="utf-8") if CHANGELOG_PATH.exists() else ""

    roadmap_after, roadmap_changed = update_roadmap(roadmap_before, metadata, roles)
    todo_after, todo_changed = update_todo(todo_before, metadata, roles)
    changelog_after, changelog_changed = update_changelog(changelog_before, metadata, roles)

    any_changed = roadmap_changed or todo_changed or changelog_changed

    print(f"PR #{metadata.number}: inferred roles -> {', '.join(roles)}")
    print(
        "Changed files: "
        + ", ".join(metadata.changed_files[:10])
        + (" ..." if len(metadata.changed_files) > 10 else "")
    )
    print(f"Will update docs: {any_changed}")

    if args.dry_run:
        return 0

    if roadmap_changed:
        ROADMAP_PATH.write_text(roadmap_after, encoding="utf-8")
    if todo_changed:
        TODO_PATH.write_text(todo_after, encoding="utf-8")
    if changelog_changed:
        CHANGELOG_PATH.write_text(changelog_after, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
