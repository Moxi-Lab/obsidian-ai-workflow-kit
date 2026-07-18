from __future__ import annotations

import argparse
import re
from pathlib import Path

from .config import (
    AI_LAYOUT_REFERENCE_REPLACEMENTS,
    AI_LAYOUT_RENAMES,
    LEGACY_STATIC_RENAMES,
    LEGACY_STATUS_MAPS,
    PROJECT_ENTRY_CURRENT_STATUSES,
    STATUS_TYPE_POLICIES,
    language_target_path,
)
from .health import detect_vault_language, read_frontmatter
from .utils import iter_markdown_files, vault_root


def replace_frontmatter_scalar(text: str, key: str, value: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    frontmatter = text[:end]
    pattern = re.compile(rf"^{re.escape(key)}:\s*.*$", re.M)
    if pattern.search(frontmatter):
        frontmatter = pattern.sub(f"{key}: {value}", frontmatter, count=1)
    else:
        frontmatter = f"{frontmatter}\n{key}: {value}"
    return f"{frontmatter}{text[end:]}"


def add_frontmatter_scalar_after(text: str, after_key: str, key: str, value: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    frontmatter = text[:end]
    if re.search(rf"^{re.escape(key)}:\s*", frontmatter, re.M):
        return text
    pattern = re.compile(rf"^({re.escape(after_key)}:\s*.*)$", re.M)
    if pattern.search(frontmatter):
        frontmatter = pattern.sub(rf"\1\n{key}: {value}", frontmatter, count=1)
    else:
        frontmatter = f"{frontmatter}\n{key}: {value}"
    return f"{frontmatter}{text[end:]}"

def collect_codex_name_migrations(root: Path) -> list[tuple[Path, Path]]:
    migrations = []
    for old_rel, new_rel in LEGACY_STATIC_RENAMES.items():
        old = root / old_rel
        if old.exists():
            migrations.append((old, root / new_rel))
    for old in sorted(root.rglob("CODEX-BRIDGE-*.md")):
        new = old.with_name(old.name.replace("CODEX-BRIDGE-", "BRIDGE-", 1))
        migrations.append((old, new))
    return migrations


def collect_ai_layout_migrations(root: Path) -> list[tuple[Path, Path]]:
    migrations = []
    for old_rel, new_rel in AI_LAYOUT_RENAMES.items():
        old = root / old_rel
        if old.exists():
            migrations.append((old, root / new_rel))
    return migrations


def rewrite_ai_layout_references(text: str) -> str:
    updated = text
    for old, new in AI_LAYOUT_REFERENCE_REPLACEMENTS:
        updated = updated.replace(old, new)
    updated = re.sub(r"(?<!00-AI/)scripts/", "00-AI/scripts/", updated)
    updated = re.sub(r"(?<!00-AI/)START-HERE\.md", "00-AI/START-HERE.md", updated)
    updated = re.sub(r"(?<!00-AI/)AGENTS\.md", "00-AI/AGENTS.md", updated)
    return updated


def migrate_ai_layout(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    migrations = collect_ai_layout_migrations(root)
    for old, new in migrations:
        old_display = old.relative_to(root).as_posix()
        new_display = new.relative_to(root).as_posix()
        if new.exists():
            print(f"skip move, target exists: {old_display} -> {new_display}")
            continue
        if args.dry_run:
            print(f"would move {old_display} -> {new_display}")
            continue
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        print(f"moved {old_display} -> {new_display}")

    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        updated = rewrite_ai_layout_references(text)
        if updated == text:
            continue
        rel = path.relative_to(root).as_posix()
        if args.dry_run:
            print(f"would update references in {rel}")
            continue
        path.write_text(updated, encoding="utf-8")
        print(f"updated references in {rel}")
    return 0


def migrate_codex_names(args: argparse.Namespace) -> int:
    root = vault_root(args.vault)
    migrations = collect_codex_name_migrations(root)
    replacements = {
        old.relative_to(root).as_posix(): new.relative_to(root).as_posix()
        for old, new in migrations
    }
    replacements.update(
        {
            "CODEX-BRIDGE-": "BRIDGE-",
            "TPL-Codex项目桥接卡.md": "TPL-project-bridge-card.md",
            "TPL-Agent交接卡.md": "TPL-agent-handoff-card.md",
            "TPL-WebClip-最简模板.md": "TPL-web-clip-minimal.md",
            "TPL-任务状态卡.md": "TPL-task-state-card.md",
            "TPL-资料分析卡.md": "TPL-source-analysis-card.md",
            "TPL-问题事故经验卡.md": "TPL-incident-experience-card.md",
            "TPL-问题知识卡-经验资产卡.md": "TPL-question-knowledge-experience-asset-card.md",
            "TPL-验收记录.md": "TPL-acceptance-record.md",
            "AI知识库复利维护SOP-v1.md": "ai-vault-maintenance-sop-v1.md",
            "Codex项目经验资产化机制-v1.md": "project-lesson-promotion-v1.md",
            "元数据最小标准-v1.md": "metadata-minimum-standard-v1.md",
            "标签与召回字段设计-v1.md": "tags-and-recall-fields-v1.md",
            "知识库巡检清单-v1.md": "vault-health-checklist-v1.md",
            "跨项目多窗口协作写作规范-v2.1.md": "multi-agent-collaboration-writing-v2.1.md",
            "codex-project-bridge": "project-bridge",
        }
    )

    for old, new in migrations:
        old_display = old.relative_to(root).as_posix()
        new_display = new.relative_to(root).as_posix()
        if new.exists():
            print(f"skip rename, target exists: {old_display} -> {new_display}")
            continue
        if args.dry_run:
            print(f"would rename {old_display} -> {new_display}")
            continue
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        print(f"renamed {old_display} -> {new_display}")

    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated == text:
            continue
        rel = path.relative_to(root).as_posix()
        if args.dry_run:
            print(f"would update references in {rel}")
            continue
        path.write_text(updated, encoding="utf-8")
        print(f"updated references in {rel}")
    return 0


def migrate_v09(args: argparse.Namespace) -> int:
    """Preview or apply the v0.8 -> v0.9 metadata and local-task migration."""
    root = vault_root(args.vault)
    language = detect_vault_language(root)
    old_task_root = root / language_target_path(language, "01-Inbox/dispatch-cards")
    new_task_root = root / language_target_path(language, "01-Inbox/tasks")

    moves: list[tuple[Path, Path]] = []
    if old_task_root.exists():
        for old in sorted(path for path in old_task_root.rglob("*") if path.is_file() and path.name != ".gitkeep"):
            new = new_task_root / old.relative_to(old_task_root)
            moves.append((old, new))
    conflicts = [(old, new) for old, new in moves if new.exists()]
    if conflicts:
        details = ", ".join(
            f"{old.relative_to(root).as_posix()} -> {new.relative_to(root).as_posix()}"
            for old, new in conflicts
        )
        raise SystemExit(f"v0.9 migration would overwrite existing task files; no changes made: {details}")

    projects_root = root / language_target_path(language, "10-Projects")
    bridge_updates: list[Path] = []
    if projects_root.exists():
        for project_dir in sorted(path for path in projects_root.iterdir() if path.is_dir()):
            current_bridges = []
            existing_entries = []
            for path in project_dir.glob("*.md"):
                metadata, _text = read_frontmatter(path)
                if metadata.get("project_entry") == "true":
                    existing_entries.append(path)
                status = metadata.get("status", "")
                effective_status = LEGACY_STATUS_MAPS["project"].get(status, status)
                if metadata.get("type") == "project-bridge" and effective_status in PROJECT_ENTRY_CURRENT_STATUSES:
                    current_bridges.append(path)
            if existing_entries:
                continue
            if len(current_bridges) > 1:
                names = ", ".join(path.name for path in current_bridges)
                raise SystemExit(
                    f"v0.9 migration found multiple current bridge cards in "
                    f"{project_dir.relative_to(root).as_posix()}; no changes made: {names}"
                )
            if len(current_bridges) == 1:
                bridge_updates.append(current_bridges[0])

    old_display = language_target_path(language, "01-Inbox/dispatch-cards").as_posix()
    new_display = language_target_path(language, "01-Inbox/tasks").as_posix()
    changed_files = 0

    for old, new in moves:
        if args.dry_run:
            print(f"would move {old.relative_to(root).as_posix()} -> {new.relative_to(root).as_posix()}")
        else:
            new.parent.mkdir(parents=True, exist_ok=True)
            old.rename(new)
            print(f"moved {old.relative_to(root).as_posix()} -> {new.relative_to(root).as_posix()}")

    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        metadata, _ = read_frontmatter(path)
        page_type = metadata.get("type", "")
        policy = STATUS_TYPE_POLICIES.get(page_type)
        updated = text
        if page_type == "task_card":
            updated = replace_frontmatter_scalar(updated, "type", "local-task")
            policy = "local_task"
        status = metadata.get("status", "")
        mapped = LEGACY_STATUS_MAPS.get(policy or "", {}).get(status)
        if mapped:
            updated = replace_frontmatter_scalar(updated, "status", mapped)
        updated = updated.replace(old_display, new_display)
        if updated == text:
            continue
        rel = path.relative_to(root).as_posix()
        changed_files += 1
        if args.dry_run:
            print(f"would update v0.9 metadata or task references in {rel}")
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"updated v0.9 metadata or task references in {rel}")

    for path in bridge_updates:
        text = path.read_text(encoding="utf-8")
        updated = add_frontmatter_scalar_after(text, "project", "pillar", "general")
        updated = add_frontmatter_scalar_after(updated, "pillar", "project_entry", "true")
        rel = path.relative_to(root).as_posix()
        changed_files += 1
        if args.dry_run:
            print(f"would add project_entry metadata in {rel}")
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"added project_entry metadata in {rel}")

    if old_task_root.exists():
        gitkeep = old_task_root / ".gitkeep"
        if args.dry_run:
            print(f"would remove empty legacy task directory {old_task_root.relative_to(root).as_posix()}")
        else:
            if gitkeep.exists() and gitkeep.is_file() and not gitkeep.read_text(encoding="utf-8").strip():
                gitkeep.unlink()
            for directory in sorted(
                (path for path in old_task_root.rglob("*") if path.is_dir()),
                key=lambda path: len(path.parts),
                reverse=True,
            ):
                if not any(directory.iterdir()):
                    directory.rmdir()
            if old_task_root.exists() and not any(old_task_root.iterdir()):
                old_task_root.rmdir()

    action = "would change" if args.dry_run else "changed"
    print(f"summary: {len(moves)} task files {action} location, {changed_files} Markdown files {action}")
    return 0
