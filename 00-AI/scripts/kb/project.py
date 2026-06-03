from __future__ import annotations

import argparse
import datetime as dt

from .utils import validate_slug, vault_root, write_file

def new_project(args: argparse.Namespace) -> int:
    validate_slug(args.slug)
    root = vault_root(args.vault)
    project_dir = root / "10-Projects" / args.slug
    if project_dir.exists() and any(project_dir.iterdir()):
        raise SystemExit(f"project directory already exists: {project_dir}")

    today = dt.date.today().isoformat()
    root_hint = args.root or "<your-project-path>"
    bridge_name = f"BRIDGE-{args.slug}.md"
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
type: project-bridge
status: active
project: {args.name}
local_root: "{root_hint}"
kb_project: "10-Projects/{args.slug}/README.md"
startup_files:
  - "00-AI/START-HERE.md"
  - "10-Projects/{args.slug}/current-state.md"
  - "10-Projects/{args.slug}/decisions.md"
updated: {today}
---

# Project Bridge | {args.name}

## One-line Purpose

Explain how this local project maps to the vault and why it matters.

## Startup Files

1. `00-AI/START-HERE.md`
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

