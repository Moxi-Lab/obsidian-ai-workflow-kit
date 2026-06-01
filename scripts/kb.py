#!/usr/bin/env python3
"""Small helpers for Obsidian AI Memory Kit."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import urllib.parse
from pathlib import Path


CORE_PATHS = [
    "START-HERE.md",
    "index.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "MIGRATION.md",
    "VERSION",
    "01-Inbox/README.md",
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


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"would create {path}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"created {path}")


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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
