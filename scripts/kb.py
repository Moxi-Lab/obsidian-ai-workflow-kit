#!/usr/bin/env python3
"""Small helpers for Obsidian AI Memory Kit."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
import urllib.parse
from pathlib import Path


CORE_PATHS = [
    "START-HERE.md",
    "index.md",
    "AGENTS.md",
    "00-Agent-Governance/README.md",
    "00-Agent-Governance/startup-contract.md",
    "00-Agent-Governance/write-back-rules.md",
    "00-Agent-Governance/review-gates.md",
    "00-Agent-Governance/maintenance-loop.md",
    "CHANGELOG.md",
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
    "START-HERE.md",
    "index.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE.md",
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
    "scripts/README.md",
    "scripts/kb.py",
]

SKIP_INSTALL_PARTS = {".git", "__pycache__"}


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian AI Memory Kit helper")
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
