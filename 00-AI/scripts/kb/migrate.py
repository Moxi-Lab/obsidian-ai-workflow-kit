from __future__ import annotations

import argparse
import re
from pathlib import Path

from .config import AI_LAYOUT_REFERENCE_REPLACEMENTS, AI_LAYOUT_RENAMES, LEGACY_STATIC_RENAMES
from .utils import iter_markdown_files, vault_root

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


