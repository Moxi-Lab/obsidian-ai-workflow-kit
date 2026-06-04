from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

from .config import (
    ADAPTER_POLICY_FILE,
    DEFAULT_INSTALL_MODE,
    MANIFEST_DIR,
    MANIFEST_FILE,
    MANIFEST_SCHEMA,
    SKIP_INSTALL_PARTS,
    install_paths_for_mode,
    language_for_install,
    language_for_upgrade,
    language_source_path,
    language_target_path,
    localize_text_references,
)
from .utils import file_sha256, repo_root


TEXT_INSTALL_SUFFIXES = {".md", ".txt", ".json", ".csv", ".yml", ".yaml"}

def read_kit_version(root: Path) -> str:
    version_file = root / "VERSION"
    if not version_file.exists():
        return "unknown"
    return version_file.read_text(encoding="utf-8").strip() or "unknown"


def manifest_path(root: Path) -> Path:
    return root / MANIFEST_DIR / MANIFEST_FILE


def adapter_policy_path(root: Path) -> Path:
    return root / MANIFEST_DIR / ADAPTER_POLICY_FILE


def load_adapter_policy(root: Path) -> dict | None:
    path = adapter_policy_path(root)
    if not path.exists():
        return None
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid kit adapter policy: {path}: {exc}") from exc
    if not isinstance(policy, dict):
        raise SystemExit(f"invalid kit adapter policy: {path}")
    return policy


def enforce_adapter_write_policy(target_root: Path, args: argparse.Namespace) -> None:
    if getattr(args, "dry_run", False) or getattr(args, "allow_protected_adapter_write", False):
        return
    policy = load_adapter_policy(target_root)
    if not policy:
        return
    if policy.get("mode") == "local-adapter" and policy.get("allow_public_kit_writes") is False:
        policy_rel = adapter_policy_path(target_root).relative_to(target_root).as_posix()
        raise SystemExit(
            "target vault is protected as a local adapter; refusing to write public kit files. "
            f"Policy: {policy_rel}. Use --dry-run for review, then adapt changes manually."
        )


def load_manifest(root: Path) -> dict:
    path = manifest_path(root)
    if not path.exists():
        return {"schema": MANIFEST_SCHEMA, "kit": "obsidian-ai-workflow-kit", "files": {}}
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid kit manifest: {path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise SystemExit(f"invalid kit manifest: {path}")
    manifest.setdefault("schema", MANIFEST_SCHEMA)
    manifest.setdefault("kit", "obsidian-ai-workflow-kit")
    manifest.setdefault("files", {})
    return manifest


def save_manifest(root: Path, manifest: dict, source_root: Path, mode: str, dry_run: bool, language: str | None = None) -> None:
    manifest["schema"] = MANIFEST_SCHEMA
    manifest["kit"] = "obsidian-ai-workflow-kit"
    manifest["source_version"] = read_kit_version(source_root)
    manifest["mode"] = mode
    if language is not None:
        manifest["language"] = language
    else:
        manifest.setdefault("language", "en")
    manifest["updated_at"] = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    path = manifest_path(root)
    if dry_run:
        print(f"would update {path.relative_to(root).as_posix()}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def record_managed_file(manifest: dict, relative: Path, source_hash: str) -> None:
    files = manifest.setdefault("files", {})
    files[relative.as_posix()] = {"sha256": source_hash}


def iter_install_files(source_root: Path, rel: str, language: str):
    source = source_root / rel
    if not source.exists():
        return
    if source.is_file():
        relative = Path(rel)
        yield language_source_path(source_root, language, relative), language_target_path(language, relative)
        return
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_INSTALL_PARTS for part in path.parts):
            continue
        if path.name in {".DS_Store"} or path.suffix == ".pyc":
            continue
        relative = path.relative_to(source_root)
        yield language_source_path(source_root, language, relative), language_target_path(language, relative)


def rendered_install_bytes(source: Path, language: str) -> bytes:
    raw = source.read_bytes()
    if source.suffix not in TEXT_INSTALL_SUFFIXES:
        return raw
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    return localize_text_references(text, language).encode("utf-8")


def rendered_install_hash(source: Path, language: str) -> str:
    return hashlib.sha256(rendered_install_bytes(source, language)).hexdigest()


def write_rendered_install_file(source: Path, target: Path, language: str) -> None:
    target.write_bytes(rendered_install_bytes(source, language))


def install_core(args: argparse.Namespace) -> int:
    source_root = repo_root()
    target_root = Path(args.target).expanduser().resolve()
    mode = getattr(args, "mode", DEFAULT_INSTALL_MODE)
    if target_root == source_root:
        raise SystemExit("target is already this kit repository; choose your own Obsidian vault path")
    try:
        target_root.relative_to(source_root)
        raise SystemExit("target cannot be inside this kit repository")
    except ValueError:
        pass
    enforce_adapter_write_policy(target_root, args)

    summary = {"created": 0, "updated": 0, "skipped": 0}
    manifest = load_manifest(target_root)
    language = language_for_install(args)
    if args.dry_run:
        print(f"would install core files into {target_root}")
        print(f"language: {language}")
    else:
        target_root.mkdir(parents=True, exist_ok=True)

    for rel in install_paths_for_mode(mode):
        for source, relative in iter_install_files(source_root, rel, language):
            target = target_root / relative
            display = str(relative)
            source_hash = rendered_install_hash(source, language)
            if target.exists() and not args.overwrite:
                summary["skipped"] += 1
                print(f"skip existing {display}")
                if file_sha256(target) == source_hash:
                    record_managed_file(manifest, relative, source_hash)
                continue
            action = "update" if target.exists() else "create"
            if args.dry_run:
                print(f"would {action} {display}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                write_rendered_install_file(source, target, language)
                print(f"{action}d {display}")
                record_managed_file(manifest, relative, source_hash)
            summary["updated" if action == "update" else "created"] += 1

    save_manifest(target_root, manifest, source_root, mode, args.dry_run, language)

    print(
        "summary: "
        f"{summary['created']} created, "
        f"{summary['updated']} updated, "
        f"{summary['skipped']} skipped"
    )
    return 0


def upgrade_core(args: argparse.Namespace) -> int:
    source_root = repo_root()
    target_root = Path(args.target).expanduser().resolve()
    mode = getattr(args, "mode", DEFAULT_INSTALL_MODE)
    if not target_root.exists():
        raise SystemExit(f"target vault does not exist: {target_root}")
    if target_root == source_root:
        raise SystemExit("target is already this kit repository; choose your own Obsidian vault path")
    enforce_adapter_write_policy(target_root, args)

    manifest = load_manifest(target_root)
    language = language_for_upgrade(args, manifest)
    managed_files = manifest.setdefault("files", {})
    stamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    summary = {
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "skipped": 0,
        "conflicts": 0,
        "candidates": 0,
    }

    if args.dry_run:
        print(f"would upgrade core files in {target_root}")
        print(f"language: {language}")

    for rel in install_paths_for_mode(mode):
        for source, relative in iter_install_files(source_root, rel, language):
            target = target_root / relative
            display = relative.as_posix()
            source_hash = rendered_install_hash(source, language)

            if not target.exists():
                summary["created"] += 1
                if args.dry_run:
                    print(f"would create {display}")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    write_rendered_install_file(source, target, language)
                    record_managed_file(manifest, relative, source_hash)
                    print(f"created {display}")
                continue

            target_hash = file_sha256(target)
            if target_hash == source_hash:
                summary["unchanged"] += 1
                record_managed_file(manifest, relative, source_hash)
                print(f"unchanged {display}")
                continue

            previous_hash = managed_files.get(display, {}).get("sha256")
            can_update = args.overwrite or (previous_hash and target_hash == previous_hash)
            if can_update:
                summary["updated"] += 1
                action = "overwrite" if args.overwrite and target_hash != previous_hash else "update"
                if args.dry_run:
                    print(f"would {action} {display}")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    write_rendered_install_file(source, target, language)
                    record_managed_file(manifest, relative, source_hash)
                    print(f"{action}d {display}")
                continue

            summary["conflicts"] += 1
            reason = "modified" if previous_hash else "unmanaged"
            print(f"skip {reason} {display}")
            if args.conflict_copy:
                candidate = target.with_name(f"{target.name}.kit-update-{stamp}")
                summary["candidates"] += 1
                if args.dry_run:
                    print(f"would write candidate {candidate.relative_to(target_root).as_posix()}")
                else:
                    write_rendered_install_file(source, candidate, language)
                    print(f"wrote candidate {candidate.relative_to(target_root).as_posix()}")
            else:
                summary["skipped"] += 1

    save_manifest(target_root, manifest, source_root, mode, args.dry_run, language)
    print(
        "summary: "
        f"{summary['created']} created, "
        f"{summary['updated']} updated, "
        f"{summary['unchanged']} unchanged, "
        f"{summary['conflicts']} conflicts, "
        f"{summary['candidates']} candidates, "
        f"{summary['skipped']} skipped"
    )
    return 0
