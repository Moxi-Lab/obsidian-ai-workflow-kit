#!/usr/bin/env python3
"""Small helpers for Obsidian AI Workflow Kit."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import sys
import urllib.parse
from pathlib import Path


CORE_PATHS = [
    "install.sh",
    "START-HERE.md",
    "index.md",
    "AGENTS.md",
    "00-Agent-Governance/README.md",
    "00-Agent-Governance/startup-contract.md",
    "00-Agent-Governance/write-back-rules.md",
    "00-Agent-Governance/review-gates.md",
    "00-Agent-Governance/maintenance-loop.md",
    "CHANGELOG.md",
    "LICENSE",
    "CONTENT-LICENSE.md",
    "MIGRATION.md",
    "VERSION",
    "01-Inbox/README.md",
    "02-Knowledge-Pipeline/README.md",
    "02-Knowledge-Pipeline/local-material-intake.md",
    "02-Knowledge-Pipeline/source-to-knowledge-workflow.md",
    "03-Recall-System/README.md",
    "03-Recall-System/task-to-context-map.md",
    "03-Recall-System/recall-fields.md",
    "10-Projects/PROJECTS-REGISTRY.md",
    "10-Projects/README.md",
    "20-SharedAssets/README.md",
    "40-ExternalSources/README.md",
    "90-Templates/TPL-Codex项目桥接卡.md",
    "90-Templates/TPL-问题事故经验卡.md",
]

STALE_PATTERNS = [
    "KB" + "-MANIFEST",
    "context" + " pack",
    "Context" + " Pack",
    "\u56db\u5927" + "\u4e3b\u7ebf",
    "LLM" + "-Wiki-Lab",
    "M" + "OC-example-projects",
    "01-" + "\u6536\u4ef6\u7bb1",
    "20-" + "\u5171\u4eab\u8d44\u4ea7",
    "40-" + "\u5916\u90e8\u8d44\u6599",
    "00-Agent" + "\u534f\u4f5c",
]

INSTALL_CORE_PATHS = [
    "README.md",
    "README.zh-CN.md",
    "RELEASE_CHECKLIST.md",
    "install.sh",
    "START-HERE.md",
    "index.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "CONTENT-LICENSE.md",
    "MIGRATION.md",
    "NOTICE.md",
    "VERSION",
    "00-Agent-Governance",
    "01-Inbox",
    "02-Knowledge-Pipeline",
    "03-Recall-System",
    "10-Projects",
    "20-SharedAssets",
    "40-ExternalSources",
    "90-Templates",
    "examples/ai-handoff-demo",
    "examples/filled-example",
    "examples/source-to-knowledge",
    "docs",
    "scripts/README.md",
    "scripts/kb.py",
]

SKIP_INSTALL_PARTS = {".git", "__pycache__"}
FOLDER_INTAKE_IGNORE_DIRS = {
    ".git",
    ".obsidian",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "target",
}
AUDIT_REPORT_DIR = "20-SharedAssets/05-audit-reports"


def vault_root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def iter_markdown_files(root: Path):
    for path in root.rglob("*.md"):
        if ".git" not in path.parts:
            yield path


def has_chinese(text: str) -> bool:
    return re.search(r"[\u4e00-\u9fff]", text) is not None


def check_required_paths(root: Path) -> list[str]:
    errors = []
    for rel in CORE_PATHS:
        if not (root / rel).exists():
            errors.append(f"missing required path: {rel}")
    return errors


def check_stale_patterns(root: Path) -> list[str]:
    errors = []
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for pattern in STALE_PATTERNS:
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
    checks = [
        ("required paths", check_required_paths(root)),
        ("stale concepts", check_stale_patterns(root)),
        ("markdown links", check_markdown_links(root)),
        ("english README", check_english_readme(root)),
    ]

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


def validate_slug(slug: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise SystemExit("slug must use lowercase letters, numbers, and hyphens")


def make_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "source"


def yaml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def escape_table(value: str) -> str:
    return value.replace("|", "\\|")


def format_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} B"
        size = size / 1024
    return f"{size} B"


def parse_extensions(value: str | None) -> set[str] | None:
    if not value:
        return None
    extensions = set()
    for item in value.split(","):
        ext = item.strip().lower()
        if not ext:
            continue
        extensions.add(ext if ext.startswith(".") else f".{ext}")
    return extensions or None


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"would create {path}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"created {path}")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def iter_install_files(source_root: Path, rel: str):
    source = source_root / rel
    if not source.exists():
        return
    if source.is_file():
        yield source, Path(rel)
        return
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_INSTALL_PARTS for part in path.parts):
            continue
        if path.name in {".DS_Store"} or path.suffix == ".pyc":
            continue
        yield path, path.relative_to(source_root)


def install_core(args: argparse.Namespace) -> int:
    source_root = repo_root()
    target_root = Path(args.target).expanduser().resolve()
    if target_root == source_root:
        raise SystemExit("target is already this kit repository; choose your own Obsidian vault path")
    try:
        target_root.relative_to(source_root)
        raise SystemExit("target cannot be inside this kit repository")
    except ValueError:
        pass

    summary = {"created": 0, "updated": 0, "skipped": 0}
    if args.dry_run:
        print(f"would install core files into {target_root}")
    else:
        target_root.mkdir(parents=True, exist_ok=True)

    for rel in INSTALL_CORE_PATHS:
        for source, relative in iter_install_files(source_root, rel):
            target = target_root / relative
            display = str(relative)
            if target.exists() and not args.overwrite:
                summary["skipped"] += 1
                print(f"skip existing {display}")
                continue
            action = "update" if target.exists() else "create"
            if args.dry_run:
                print(f"would {action} {display}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                print(f"{action}d {display}")
            summary["updated" if action == "update" else "created"] += 1

    print(
        "summary: "
        f"{summary['created']} created, "
        f"{summary['updated']} updated, "
        f"{summary['skipped']} skipped"
    )
    return 0


def new_project(args: argparse.Namespace) -> int:
    validate_slug(args.slug)
    root = vault_root(args.vault)
    project_dir = root / "10-Projects" / args.slug
    if project_dir.exists() and any(project_dir.iterdir()):
        raise SystemExit(f"project directory already exists: {project_dir}")

    today = dt.date.today().isoformat()
    root_hint = args.root or "<your-project-path>"
    bridge_name = f"CODEX-BRIDGE-{args.slug}.md"
    files = {
        "README.md": f"""---
type: project-readme
status: active
project: {args.name}
---

# {args.name}

## Purpose

Describe what this project is for and why an AI agent may need to resume it.

## Start Here

- `{bridge_name}`
- `current-state.md`
- `decisions.md`

## Next Action

- Define the next concrete action before starting work.
""",
        bridge_name: f"""---
type: codex-project-bridge
status: active
project: {args.name}
local_root: "{root_hint}"
kb_project: "10-Projects/{args.slug}/README.md"
startup_files:
  - "START-HERE.md"
  - "10-Projects/{args.slug}/current-state.md"
  - "10-Projects/{args.slug}/decisions.md"
updated: {today}
---

# Project Bridge | {args.name}

## One-line Purpose

Explain how this local project maps to the vault and why it matters.

## Startup Files

1. `START-HERE.md`
2. This bridge card
3. `current-state.md`
4. `decisions.md`

## Current State

- {today}: Initial bridge card created.

## Recent Decisions

- No stable decisions recorded yet.

## Next Startup

- Read this bridge card and update `current-state.md` before changing project files.

## Write-back Rules

| Content | Write Back To |
|---|---|
| Long-term project state | This bridge card or `current-state.md` |
| Stable decisions | `decisions.md` |
| Short handoff | `01-Inbox/agent-handoffs/` |
| Reusable lesson | `20-SharedAssets/02-modules/` |
""",
        "current-state.md": f"""---
type: project-state
status: active
project: {args.name}
updated: {today}
---

# Current State | {args.name}

- {today}: Project workspace created.
""",
        "decisions.md": f"""---
type: decisions
status: active
project: {args.name}
updated: {today}
---

# Decisions | {args.name}

No stable decisions recorded yet.
""",
    }

    if args.dry_run:
        print(f"would create directory {project_dir}")
    else:
        project_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in files.items():
        write_file(project_dir / filename, content, args.dry_run)
    return 0


def intake_source(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    title = args.title or Path(args.source).stem or "Untitled Source"
    slug = make_slug(args.slug or title)
    target_dir = root / "40-ExternalSources" / "01-samples"
    target = target_dir / f"{slug}.md"
    if target.exists() and not args.force:
        raise SystemExit(f"source card already exists: {target}")

    today = dt.date.today().isoformat()
    project = args.project or ""
    content = f"""---
type: source-analysis
status: inbox
title: "{title}"
source: "{args.source}"
captured: {today}
related_project: "{project}"
themes: []
canonical: false
---

# Source Analysis | {title}

## Source

- Source: `{args.source}`
- Related project: `{project}`
- Captured: {today}

## One-line Summary

To be filled by AI after reading the source.

## Key Points

-

## Useful For

-

## Write-back Target

- Keep this source card in `40-ExternalSources/` as evidence.
- If it changes project state, update `10-Projects/<project>/current-state.md`.
- If it creates a stable decision, update `10-Projects/<project>/decisions.md`.
- If it becomes reusable knowledge, create a question knowledge card / experience asset or write to `20-SharedAssets/02-modules/`.
- If it must be recalled before future tasks, update the matching project bridge card or `03-Recall-System/task-to-context-map.md`.

## Next AI Action

Read the source, summarize it without copying the full text, then decide whether it should stay as source analysis or be promoted. Do not move this source card when promoting; keep it as non-canonical evidence and create or update the promoted target separately.
"""

    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
    write_file(target, content, args.dry_run)
    return 0


def collect_folder_files(
    source: Path,
    *,
    include_hidden: bool,
    extensions: set[str] | None,
    max_files: int,
) -> tuple[list[Path], dict[str, int]]:
    stats = {
        "matched": 0,
        "listed": 0,
        "omitted_after_limit": 0,
        "skipped_hidden": 0,
        "skipped_ignored_dirs": 0,
        "skipped_by_extension": 0,
    }
    listed: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(source):
        kept_dirs = []
        for dirname in sorted(dirnames):
            if dirname in FOLDER_INTAKE_IGNORE_DIRS:
                stats["skipped_ignored_dirs"] += 1
                continue
            if not include_hidden and dirname.startswith("."):
                stats["skipped_hidden"] += 1
                continue
            kept_dirs.append(dirname)
        dirnames[:] = kept_dirs

        for filename in sorted(filenames):
            if not include_hidden and filename.startswith("."):
                stats["skipped_hidden"] += 1
                continue
            path = Path(dirpath) / filename
            if extensions is not None and path.suffix.lower() not in extensions:
                stats["skipped_by_extension"] += 1
                continue
            stats["matched"] += 1
            if len(listed) >= max_files:
                stats["omitted_after_limit"] += 1
                continue
            listed.append(path)
            stats["listed"] += 1
    return listed, stats


def intake_folder(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    source = Path(args.folder).expanduser().resolve()
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"folder does not exist or is not a directory: {source}")
    if args.max_files < 1:
        raise SystemExit("max-files must be at least 1")

    title = args.title or source.name or "Folder Intake"
    slug = make_slug(args.slug or title)
    target_dir = root / "40-ExternalSources" / "02-folder-intakes"
    target = target_dir / f"{slug}.md"
    if target.exists() and not args.force:
        raise SystemExit(f"folder intake already exists: {target}")

    extensions = parse_extensions(args.extensions)
    listed, stats = collect_folder_files(
        source,
        include_hidden=args.include_hidden,
        extensions=extensions,
        max_files=args.max_files,
    )
    today = dt.date.today().isoformat()
    rows = []
    for path in listed:
        rel = path.relative_to(source).as_posix()
        stat = path.stat()
        modified = dt.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        rows.append(f"| `{escape_table(rel)}` | {format_size(stat.st_size)} | {modified} |")
    if not rows:
        rows.append("| _No files listed_ | - | - |")

    extension_note = ", ".join(sorted(extensions)) if extensions else "all"
    content = f"""---
type: folder-intake
status: inbox
title: {yaml_string(title)}
source_folder: {yaml_string(str(source))}
captured: {today}
related_project: {yaml_string(args.project or "")}
file_count: {stats["matched"]}
listed_count: {stats["listed"]}
omitted_count: {stats["omitted_after_limit"]}
canonical: false
---

# Folder Intake | {title}

## Source Folder

- Path: `{source}`
- Related project: `{args.project or ""}`
- Captured: {today}
- Extension filter: `{extension_note}`
- Original files remain in place. This card is only an intake manifest.

## File Inventory

| Path | Size | Modified |
|---|---:|---|
{chr(10).join(rows)}

## Skipped / Omitted

- Hidden files or directories skipped: {stats["skipped_hidden"]}
- Ignored tool directories skipped: {stats["skipped_ignored_dirs"]}
- Files skipped by extension filter: {stats["skipped_by_extension"]}
- Files omitted after `max_files`: {stats["omitted_after_limit"]}

## Next AI Action

1. Review this manifest before reading file contents.
2. Ask the user which subset should be processed first if the folder is broad.
3. Use `02-Knowledge-Pipeline/local-material-intake.md` before creating long-term notes.
4. Keep original files in place; promote only stable summaries, decisions, or reusable lessons.
"""

    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
    write_file(target, content, args.dry_run)
    return 0


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


def project_dirs_without_bridge(root: Path) -> list[str]:
    projects_root = root / "10-Projects"
    missing = []
    if not projects_root.exists():
        return missing
    for path in sorted(projects_root.iterdir()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if not list(path.glob("CODEX-BRIDGE-*.md")):
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian AI Workflow Kit helper")
    parser.add_argument("--vault", help="Vault root. Defaults to current directory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    health = subparsers.add_parser("health-check", help="Run repository checks")
    health.add_argument("--vault", help="Vault root. Defaults to current directory.")
    health.set_defaults(func=health_check)

    new = subparsers.add_parser("new-project", help="Create a project workspace")
    new.add_argument("slug", help="Directory slug, for example my-project")
    new.add_argument("--vault", help="Vault root. Defaults to current directory.")
    new.add_argument("--name", required=True, help="Project display name")
    new.add_argument("--root", help="Local project path to record in the bridge card")
    new.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    new.set_defaults(func=new_project)

    intake = subparsers.add_parser("intake-source", help="Create a source analysis card")
    intake.add_argument("source", help="Local file path, folder path, or URL")
    intake.add_argument("--vault", help="Vault root. Defaults to current directory.")
    intake.add_argument("--title", help="Source title. Defaults to source filename.")
    intake.add_argument("--project", help="Related project slug or name")
    intake.add_argument("--slug", help="Output filename slug")
    intake.add_argument("--force", action="store_true", help="Overwrite an existing source card")
    intake.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    intake.set_defaults(func=intake_source)

    intake_folder_parser = subparsers.add_parser("intake-folder", help="Create a folder intake manifest")
    intake_folder_parser.add_argument("folder", help="Local folder to inventory")
    intake_folder_parser.add_argument("--vault", help="Vault root. Defaults to current directory.")
    intake_folder_parser.add_argument("--title", help="Manifest title. Defaults to folder name.")
    intake_folder_parser.add_argument("--project", help="Related project slug or name")
    intake_folder_parser.add_argument("--slug", help="Output filename slug")
    intake_folder_parser.add_argument("--extensions", help="Comma-separated extension filter, for example md,pdf,txt")
    intake_folder_parser.add_argument("--max-files", type=int, default=200, help="Maximum files to list")
    intake_folder_parser.add_argument("--include-hidden", action="store_true", help="Include hidden files and folders")
    intake_folder_parser.add_argument("--force", action="store_true", help="Overwrite an existing manifest")
    intake_folder_parser.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    intake_folder_parser.set_defaults(func=intake_folder)

    audit = subparsers.add_parser("audit-vault", help="Audit vault structure without changing notes")
    audit.add_argument("--vault", help="Vault root. Defaults to current directory.")
    audit.add_argument("--write-report", action="store_true", help="Write an audit report into the vault")
    audit.set_defaults(func=audit_vault)

    install = subparsers.add_parser("install-core", help="Install the kit into another Obsidian vault")
    install.add_argument("target", help="Target Obsidian vault directory")
    install.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    install.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    install.set_defaults(func=install_core)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
