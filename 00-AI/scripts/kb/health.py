from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.parse
from pathlib import Path

from .config import (
    AUDIT_REPORT_DIR,
    DEFAULT_STALE_PATTERNS_FILE,
    MANIFEST_DIR,
    MANIFEST_FILE,
    VAULT_STALE_PATTERNS_FILE,
    DEFAULT_LANGUAGE,
    language_target_path,
    required_paths_for_mode,
    validate_language,
)
from .utils import has_chinese, iter_markdown_files, read_frontmatter_value, vault_root


def read_stale_pattern_file(path: Path) -> list[str]:
    patterns: list[str] = []
    if not path.exists():
        return patterns
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        patterns.append(stripped)
    return patterns


def load_stale_patterns(root: Path) -> list[str]:
    override = root / VAULT_STALE_PATTERNS_FILE
    if override.exists():
        return read_stale_pattern_file(override)
    language = detect_vault_language(root)
    return read_stale_pattern_file(root / language_target_path(language, DEFAULT_STALE_PATTERNS_FILE))


def detect_vault_language(root: Path) -> str:
    path = root / MANIFEST_DIR / MANIFEST_FILE
    if not path.exists():
        return DEFAULT_LANGUAGE
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_LANGUAGE
    if not isinstance(manifest, dict):
        return DEFAULT_LANGUAGE
    try:
        return validate_language(manifest.get("language"))
    except SystemExit:
        return DEFAULT_LANGUAGE


def check_required_paths(root: Path, mode: str = "full", language: str | None = None) -> list[str]:
    selected_language = language or detect_vault_language(root)
    errors = []
    for rel in required_paths_for_mode(mode, selected_language):
        if not (root / rel).exists():
            errors.append(f"missing required path: {rel}")
    return errors


def check_stale_patterns(root: Path) -> list[str]:
    errors = []
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for pattern in load_stale_patterns(root):
            if pattern in text:
                rel = path.relative_to(root)
                errors.append(f"stale concept in {rel}: {pattern}")
    return errors


def check_markdown_links(root: Path) -> list[str]:
    errors = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for match in link_pattern.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / urllib.parse.unquote(target)).resolve()
            if not str(resolved).startswith(str(root)):
                errors.append(f"link escapes vault: {path.relative_to(root)} -> {target}")
            elif not resolved.exists():
                errors.append(f"broken link: {path.relative_to(root)} -> {target}")
    return errors


def check_english_readme(root: Path) -> list[str]:
    readme = root / "README.md"
    if not readme.exists():
        return ["missing README.md"]
    text = readme.read_text(encoding="utf-8")
    if has_chinese(text):
        return ["README.md contains visible Chinese text"]
    return []


def health_check(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    mode = getattr(args, "mode", "full")
    language = detect_vault_language(root)
    checks = [
        ("required paths", check_required_paths(root, mode, language)),
        ("stale concepts", check_stale_patterns(root)),
        ("markdown links", check_markdown_links(root)),
    ]
    if mode == "full":
        checks.append(("english README", check_english_readme(root)))

    failed = False
    for name, errors in checks:
        if errors:
            failed = True
            print(f"FAIL {name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {name}")
    return 1 if failed else 0


def count_inbox_files(root: Path) -> dict[str, int]:
    result = {}
    inbox_root = root / "01-Inbox"
    for rel in ["agent-handoffs", "dispatch-cards", "web-clips"]:
        folder = inbox_root / rel
        count = 0
        if folder.exists():
            for path in folder.rglob("*"):
                if not path.is_file():
                    continue
                if path.name in {".gitkeep", "README.md"}:
                    continue
                count += 1
        result[rel] = count
    return result


def project_bridge_cards(root: Path) -> list[Path]:
    projects_root = root / "10-Projects"
    if not projects_root.exists():
        return []
    cards = list(projects_root.rglob("BRIDGE-*.md"))
    cards.extend(projects_root.rglob("CODEX-BRIDGE-*.md"))
    return sorted(set(cards))


def build_stale_report(
    root: Path,
    *,
    max_age_days: int,
    inbox_threshold: int,
    today: dt.date | None = None,
) -> tuple[str, int]:
    today = today or dt.date.today()
    finding_count = 0
    lines = [
        "---",
        "type: stale-check-report",
        "status: draft",
        f"created: {today.isoformat()}",
        "---",
        "",
        f"# Stale Check | {today.isoformat()}",
        "",
        "## Project Bridge Freshness",
        "",
    ]

    bridge_findings = []
    for path in project_bridge_cards(root):
        rel = path.relative_to(root).as_posix()
        updated_value = read_frontmatter_value(path, "updated")
        if not updated_value:
            bridge_findings.append(f"- REVIEW `{rel}`: missing updated date")
            continue
        try:
            updated = dt.date.fromisoformat(updated_value)
        except ValueError:
            bridge_findings.append(f"- REVIEW `{rel}`: invalid updated date `{updated_value}`")
            continue
        age_days = (today - updated).days
        if age_days > max_age_days:
            bridge_findings.append(
                f"- STALE `{rel}`: updated {updated.isoformat()} "
                f"({age_days} days old, threshold {max_age_days})"
            )

    if bridge_findings:
        finding_count += len(bridge_findings)
        lines.extend(bridge_findings)
    else:
        lines.append("- No stale bridge cards.")

    lines.extend(["", "## Inbox Pile-up", ""])
    inbox_findings = []
    for rel, count in count_inbox_files(root).items():
        if count > inbox_threshold:
            inbox_findings.append(f"- WARN `{rel}`: {count} files (threshold {inbox_threshold})")

    if inbox_findings:
        finding_count += len(inbox_findings)
        lines.extend(inbox_findings)
    else:
        lines.append("- No Inbox pile-up.")

    lines.extend(
        [
            "",
            "## Recommended Next Action",
            "",
            "1. For each bridge finding, update the bridge card `updated` field, current state, recent decisions, and next startup action.",
            "2. For each Inbox warning, move or promote files that already have a destination.",
            "3. Before long work, tell the user which bridge card or Inbox folder needs maintenance.",
            "4. Write a short handoff if this session changed project state.",
        ]
    )
    return "\n".join(lines) + "\n", finding_count


def stale_check(args: argparse.Namespace) -> int:
    if args.max_age_days < 1:
        raise SystemExit("max-age-days must be at least 1")
    if args.inbox_threshold < 0:
        raise SystemExit("inbox-threshold must be at least 0")
    root = vault_root(args.vault)
    report, finding_count = build_stale_report(
        root,
        max_age_days=args.max_age_days,
        inbox_threshold=args.inbox_threshold,
    )
    print(report)
    if args.fail_on_findings and finding_count:
        return 1
    return 0


def project_dirs_without_bridge(root: Path) -> list[str]:
    projects_root = root / "10-Projects"
    missing = []
    if not projects_root.exists():
        return missing
    for path in sorted(projects_root.iterdir()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if not list(path.glob("BRIDGE-*.md")) and not list(path.glob("CODEX-BRIDGE-*.md")):
            missing.append(path.name)
    return missing


def build_audit_report(root: Path) -> tuple[str, int]:
    today = dt.date.today().isoformat()
    checks = [
        ("required paths", check_required_paths(root)),
        ("stale concepts", check_stale_patterns(root)),
        ("markdown links", check_markdown_links(root)),
        ("english README", check_english_readme(root)),
    ]
    inbox_counts = count_inbox_files(root)
    missing_bridges = project_dirs_without_bridge(root)
    issue_count = sum(len(errors) for _, errors in checks)
    issue_count += sum(inbox_counts.values())
    issue_count += len(missing_bridges)

    lines = [
        "---",
        "type: vault-audit-report",
        "status: draft",
        f"created: {today}",
        "---",
        "",
        f"# Vault Audit | {today}",
        "",
        "## Summary",
        "",
        f"- Root: `{root}`",
        f"- Issues or review items: {issue_count}",
        "",
        "## Core Checks",
        "",
    ]
    for name, errors in checks:
        if errors:
            lines.append(f"- FAIL {name}: {len(errors)}")
            lines.extend(f"  - {error}" for error in errors)
        else:
            lines.append(f"- PASS {name}")

    lines.extend(["", "## Inbox files", ""])
    for rel, count in inbox_counts.items():
        lines.append(f"- `{rel}`: {count}")

    lines.extend(["", "## Project directories without bridge", ""])
    if missing_bridges:
        lines.extend(f"- `{name}`" for name in missing_bridges)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Recommended Next Action",
            "",
            "1. Clear Inbox files that no longer need handoff.",
            "2. Add bridge cards for long-lived project directories.",
            "3. Run `health-check` after changes.",
        ]
    )
    return "\n".join(lines) + "\n", issue_count


def audit_vault(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    report, _issue_count = build_audit_report(root)
    print(report)
    if args.write_report:
        report_dir = root / AUDIT_REPORT_DIR
        report_dir.mkdir(parents=True, exist_ok=True)
        today = dt.date.today().isoformat()
        target = report_dir / f"AUDIT-{today}.md"
        if target.exists():
            stamp = dt.datetime.now().strftime("%H%M%S")
            target = report_dir / f"AUDIT-{today}-{stamp}.md"
        target.write_text(report, encoding="utf-8")
        print(f"created {target}")
    return 0
