from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path

from .config import FOLDER_INTAKE_IGNORE_DIRS, language_target_path, localize_text_references
from .utils import (
    escape_table,
    format_size,
    make_slug,
    parse_extensions,
    vault_language,
    vault_root,
    write_file,
    yaml_string,
)

def intake_source(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    language = vault_language(root)
    title = args.title or Path(args.source).stem or "Untitled Source"
    slug = make_slug(args.slug or title)
    target_dir = root / language_target_path(language, "40-ExternalSources/01-samples")
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
- If it must be recalled before future tasks, update the matching project bridge card or `00-AI/recall/task-to-context-map.md`.

## Next AI Action

Read the source, summarize it without copying the full text, then decide whether it should stay as source analysis or be promoted. Do not move this source card when promoting; keep it as non-canonical evidence and create or update the promoted target separately.
"""

    content = localize_text_references(content, language)

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
    language = vault_language(root)
    source = Path(args.folder).expanduser().resolve()
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"folder does not exist or is not a directory: {source}")
    if args.max_files < 1:
        raise SystemExit("max-files must be at least 1")

    title = args.title or source.name or "Folder Intake"
    slug = make_slug(args.slug or title)
    target_dir = root / language_target_path(language, "40-ExternalSources/02-folder-intakes")
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
3. Use `00-AI/pipeline/local-material-intake.md` before creating long-term notes.
4. Keep original files in place; promote only stable summaries, decisions, or reusable lessons.
"""

    content = localize_text_references(content, language)

    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
    write_file(target, content, args.dry_run)
    return 0

