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
    EXTERNAL_BASE_TYPES,
    LOCAL_TASK_REQUIRED_FIELDS,
    MANIFEST_DIR,
    MANIFEST_FILE,
    MANIFEST_SCHEMA,
    PROJECT_ENTRY_ALL_STATUSES,
    PROJECT_ENTRY_CURRENT_STATUSES,
    PROJECT_ENTRY_REQUIRED_FIELDS,
    PROJECT_PRIORITY_VALUES,
    STATUS_TYPE_POLICIES,
    STATUS_VALUES,
    VAULT_STALE_PATTERNS_FILE,
    DEFAULT_LANGUAGE,
    language_target_path,
    required_paths_for_mode,
    validate_language,
)
from .utils import file_sha256, has_chinese, iter_markdown_files, read_frontmatter_value, vault_root


WIKILINK_PATTERN = re.compile(r"!?(?<!\\)\[\[([^\[\]\n]+)\]\]")
PRIVATE_USER_PATH_PATTERN = re.compile(r"/Users/([^/<>{}\s\"']+)/")
PUBLIC_USER_PATH_PLACEHOLDERS = {"me", "you", "user", "username", "your-name"}


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


def detect_vault_mode(root: Path) -> str:
    path = root / MANIFEST_DIR / MANIFEST_FILE
    if not path.exists():
        return "full"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "full"
    if not isinstance(manifest, dict):
        return "full"
    mode = manifest.get("mode")
    if mode in {"full", "barebone", "shared-core"}:
        return mode
    return "full"


def check_required_paths(root: Path, mode: str = "full", language: str | None = None) -> list[str]:
    selected_language = language or detect_vault_language(root)
    errors = []
    for rel in required_paths_for_mode(mode, selected_language):
        if not (root / rel).exists():
            errors.append(f"missing required path: {rel}")
    return errors


def check_managed_manifest(root: Path, expected_mode: str | None = None) -> list[str]:
    path = root / MANIFEST_DIR / MANIFEST_FILE
    if not path.exists():
        return [f"missing managed manifest: {MANIFEST_DIR}/{MANIFEST_FILE}"]
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid managed manifest JSON: {exc}"]
    if not isinstance(manifest, dict):
        return ["managed manifest must be a JSON object"]

    errors: list[str] = []
    if manifest.get("schema") != MANIFEST_SCHEMA:
        errors.append(
            f"managed manifest schema mismatch: {manifest.get('schema') or '-'}; "
            f"expected={MANIFEST_SCHEMA}"
        )
    if manifest.get("kit") != "obsidian-ai-workflow-kit":
        errors.append(f"unexpected managed manifest kit: {manifest.get('kit') or '-'}")
    mode = manifest.get("mode")
    if expected_mode and mode != expected_mode:
        errors.append(f"managed manifest mode mismatch: {mode or '-'}; expected={expected_mode}")
    try:
        language = validate_language(manifest.get("language"))
    except SystemExit:
        errors.append(f"unsupported managed manifest language: {manifest.get('language') or '-'}")
        language = DEFAULT_LANGUAGE

    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        errors.append("managed manifest files must be a non-empty object")
        return errors

    allowed_roots: list[str] = []
    if expected_mode:
        allowed_roots = required_paths_for_mode(expected_mode, language)
    root_resolved = root.resolve()
    for rel, record in sorted(files.items()):
        if not isinstance(rel, str) or not rel:
            errors.append("managed manifest contains an invalid file path")
            continue
        relative = Path(rel)
        target = (root / relative).resolve()
        try:
            target.relative_to(root_resolved)
        except ValueError:
            errors.append(f"managed file escapes vault: {rel}")
            continue
        if allowed_roots and not any(
            rel == allowed or rel.startswith(f"{allowed}/") for allowed in allowed_roots
        ):
            errors.append(f"managed file is outside {expected_mode} scope: {rel}")
        if not isinstance(record, dict) or not isinstance(record.get("sha256"), str):
            errors.append(f"managed file has no recorded sha256: {rel}")
            continue
        if not target.is_file():
            errors.append(f"managed file is missing: {rel}")
            continue
        expected_hash = record["sha256"]
        actual_hash = file_sha256(target)
        if actual_hash != expected_hash:
            errors.append(
                f"managed file hash mismatch: {rel}; "
                f"expected={expected_hash} actual={actual_hash}"
            )
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


def read_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized = value.strip()
        if " #" in normalized:
            normalized = normalized.split(" #", 1)[0].rstrip()
        metadata[key.strip()] = normalized.strip("\"'")
    return metadata, text


def strip_code_for_link_checks(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def wikilink_index(root: Path) -> tuple[dict[str, list[Path]], dict[str, list[Path]]]:
    by_stem: dict[str, list[Path]] = {}
    by_name: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in {".git", ".obsidian", "__pycache__"} for part in path.parts):
            continue
        by_name.setdefault(path.name.casefold(), []).append(path)
        by_stem.setdefault(path.stem.casefold(), []).append(path)
    return by_stem, by_name


def check_wikilinks(root: Path) -> list[str]:
    errors: list[str] = []
    by_stem, by_name = wikilink_index(root)
    root_resolved = root.resolve()
    for path in iter_markdown_files(root):
        text = strip_code_for_link_checks(path.read_text(encoding="utf-8"))
        for match in WIKILINK_PATTERN.finditer(text):
            raw = match.group(1).split("|", 1)[0].strip()
            target = raw.split("#", 1)[0].split("^", 1)[0].strip()
            if not target or "{{" in target:
                continue
            target = urllib.parse.unquote(target)
            rel = path.relative_to(root).as_posix()
            if "/" in target or target.startswith((".", "..")):
                candidates = [root / target, path.parent / target]
                expanded = []
                for candidate in candidates:
                    expanded.append(candidate)
                    if not candidate.suffix:
                        expanded.extend([candidate.with_suffix(".md"), candidate.with_suffix(".base")])
                resolved_candidates = []
                for candidate in expanded:
                    resolved = candidate.resolve()
                    try:
                        resolved.relative_to(root_resolved)
                    except ValueError:
                        continue
                    if resolved.exists():
                        resolved_candidates.append(resolved)
                if not resolved_candidates:
                    errors.append(f"broken wikilink: {rel} -> {target}")
                continue

            key = target.casefold()
            matches = by_name.get(key, []) if Path(target).suffix else by_stem.get(key, [])
            if not matches:
                errors.append(f"broken wikilink: {rel} -> {target}")
            elif len(matches) > 1:
                choices = ", ".join(sorted(item.relative_to(root).as_posix() for item in matches))
                errors.append(f"ambiguous wikilink: {rel} -> {target} matches [{choices}]")
    return errors


def status_policy_for(path: Path, metadata: dict[str, str], root: Path) -> str:
    page_type = metadata.get("type", "")
    if page_type in STATUS_TYPE_POLICIES:
        return STATUS_TYPE_POLICIES[page_type]
    return "governance"


def check_typed_statuses(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_markdown_files(root):
        metadata, text = read_frontmatter(path)
        if not metadata:
            continue
        page_type = metadata.get("type", "")
        status = metadata.get("status", "")
        rel = path.relative_to(root).as_posix()
        if page_type and not status:
            errors.append(f"missing status for typed page: {rel}")
            continue
        if not status:
            continue
        policy = status_policy_for(path, metadata, root)
        allowed = STATUS_VALUES[policy]
        if status not in allowed:
            errors.append(
                f"unsupported {policy} status in {rel}: {status}; "
                f"allowed={','.join(sorted(allowed))}"
            )
        frontmatter_text = text[: text.find("\n---", 4)] if text.startswith("---\n") else ""
        if re.search(r"^status:\s*[\"']", frontmatter_text, re.M):
            errors.append(f"quoted status in {rel}")
    return errors


def check_base_files(root: Path, mode: str, language: str) -> list[str]:
    if mode not in {"full", "shared-core"}:
        return []
    errors: list[str] = []
    project_folder = language_target_path(language, "10-Projects").as_posix()
    task_folder = language_target_path(language, "01-Inbox/tasks").as_posix()
    source_folder = language_target_path(language, "40-ExternalSources").as_posix()
    specs = {
        "00-AI/bases/project-overview.base": [
            "filters:", "properties:", "views:", "project_entry == true", "pillar:",
            f'file.inFolder("{project_folder}")',
            *[f'status == "{status}"' for status in sorted(PROJECT_ENTRY_CURRENT_STATUSES)],
        ],
        "00-AI/bases/task-overview.base": [
            "filters:", "properties:", "views:", 'type == "local-task"',
            f'file.inFolder("{task_folder}")',
            *[f'status == "{status}"' for status in sorted(STATUS_VALUES["local_task"])],
        ],
        "00-AI/bases/source-overview.base": [
            "filters:", "properties:", "views:", "captured:",
            f'file.inFolder("{source_folder}")',
            *[f'type == "{page_type}"' for page_type in sorted(EXTERNAL_BASE_TYPES)],
        ],
    }
    for source_rel, markers in specs.items():
        rel = language_target_path(language, source_rel)
        path = root / rel
        if not path.exists():
            errors.append(f"missing Base file: {rel.as_posix()}")
            continue
        text = path.read_text(encoding="utf-8")
        if "\t" in text:
            errors.append(f"Base contains tab indentation: {rel.as_posix()}")
        for marker in markers:
            if marker not in text:
                errors.append(f"Base contract missing in {rel.as_posix()}: {marker}")
    return errors


def health_checks_for_mode(root: Path, mode: str, language: str) -> list[tuple[str, list[str]]]:
    if mode == "shared-core":
        return [
            ("required paths", check_required_paths(root, mode, language)),
            ("managed manifest", check_managed_manifest(root, expected_mode=mode)),
            ("Base files", check_base_files(root, mode, language)),
        ]
    checks = [
        ("required paths", check_required_paths(root, mode, language)),
        ("stale concepts", check_stale_patterns(root)),
        ("markdown links", check_markdown_links(root)),
        ("wikilinks", check_wikilinks(root)),
        ("typed status", check_typed_statuses(root)),
        ("Base files", check_base_files(root, mode, language)),
        ("Base dependency metadata", check_base_dependency_metadata(root, language)),
    ]
    if not (root / MANIFEST_DIR / MANIFEST_FILE).exists():
        checks.append(("private user paths", check_private_user_paths(root)))
    if mode == "full" and language == "en":
        checks.append(("english README", check_english_readme(root)))
    return checks


def check_base_dependency_metadata(root: Path, language: str) -> list[str]:
    errors: list[str] = []
    projects_root = root / language_target_path(language, "10-Projects")
    if projects_root.exists():
        for path in projects_root.rglob("*.md"):
            metadata, text = read_frontmatter(path)
            marker = metadata.get("project_entry", "")
            rel = path.relative_to(root).as_posix()
            if marker and marker not in {"true", "false"}:
                errors.append(f"invalid project_entry boolean in {rel}: {marker}")
            if marker == "true":
                missing = sorted(field for field in PROJECT_ENTRY_REQUIRED_FIELDS if not metadata.get(field))
                if missing:
                    errors.append(f"project entry missing metadata in {rel}: {', '.join(missing)}")
                if metadata.get("status") not in PROJECT_ENTRY_ALL_STATUSES:
                    errors.append(f"unsupported project entry status in {rel}: {metadata.get('status') or '-'}")
                if metadata.get("priority") not in PROJECT_PRIORITY_VALUES:
                    errors.append(f"unsupported project entry priority in {rel}: {metadata.get('priority') or '-'}")
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata.get("last_verified", "")):
                    errors.append(f"invalid project entry last_verified date in {rel}: {metadata.get('last_verified') or '-'}")
                frontmatter_text = text[: text.find("\n---", 4)] if text.startswith("---\n") else ""
                if re.search(r"^status:\s*[\"']", frontmatter_text, re.M):
                    errors.append(f"quoted project entry status in {rel}")
            if (
                metadata.get("type") in {"project-bridge", "codex-project-bridge"}
                and metadata.get("status") in PROJECT_ENTRY_CURRENT_STATUSES
                and marker != "true"
            ):
                errors.append(f"current project bridge missing project_entry: {rel}")

    task_root = root / language_target_path(language, "01-Inbox/tasks")
    if task_root.exists():
        for path in task_root.rglob("*.md"):
            metadata, _text = read_frontmatter(path)
            rel = path.relative_to(root).as_posix()
            missing = sorted(field for field in LOCAL_TASK_REQUIRED_FIELDS if not metadata.get(field))
            if missing:
                errors.append(f"local task missing metadata in {rel}: {', '.join(missing)}")
            if metadata.get("type") != "local-task":
                errors.append(f"local task missing type=local-task: {rel}")
            if metadata.get("status") not in STATUS_VALUES["local_task"]:
                errors.append(f"unsupported local task status in {rel}: {metadata.get('status') or '-'}")

    sources_root = root / language_target_path(language, "40-ExternalSources")
    if sources_root.exists():
        for path in sources_root.rglob("*.md"):
            metadata, _text = read_frontmatter(path)
            if metadata.get("type") not in EXTERNAL_BASE_TYPES:
                continue
            rel = path.relative_to(root).as_posix()
            if not metadata.get("captured"):
                errors.append(f"Base source missing captured date: {rel}")
            if metadata.get("status") not in STATUS_VALUES["external"]:
                errors.append(f"unsupported Base source status in {rel}: {metadata.get('status') or '-'}")
    return errors


def check_private_user_paths(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for match in PRIVATE_USER_PATH_PATTERN.finditer(text):
            if match.group(1).casefold() not in PUBLIC_USER_PATH_PLACEHOLDERS:
                errors.append(
                    f"private-looking user path in {path.relative_to(root).as_posix()}: /Users/{match.group(1)}/"
                )
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
    mode = getattr(args, "mode", None) or detect_vault_mode(root)
    language = detect_vault_language(root)
    checks = health_checks_for_mode(root, mode, language)

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


def count_inbox_files(root: Path, language: str | None = None) -> dict[str, int]:
    result = {}
    selected_language = language or detect_vault_language(root)
    for rel in ["agent-handoffs", "tasks", "web-clips"]:
        display = language_target_path(selected_language, f"01-Inbox/{rel}").as_posix()
        folder = root / display
        count = 0
        if folder.exists():
            for path in folder.rglob("*"):
                if not path.is_file():
                    continue
                if path.name in {".gitkeep", "README.md"}:
                    continue
                count += 1
        result[display] = count
    return result


def project_bridge_cards(root: Path, language: str | None = None) -> list[Path]:
    selected_language = language or detect_vault_language(root)
    projects_root = root / language_target_path(selected_language, "10-Projects")
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


def project_dirs_without_bridge(root: Path, language: str | None = None) -> list[str]:
    selected_language = language or detect_vault_language(root)
    projects_root = root / language_target_path(selected_language, "10-Projects")
    missing = []
    if not projects_root.exists():
        return missing
    for path in sorted(projects_root.iterdir()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if not list(path.glob("BRIDGE-*.md")) and not list(path.glob("CODEX-BRIDGE-*.md")):
            missing.append(path.name)
    return missing


def build_audit_report(root: Path, mode: str | None = None) -> tuple[str, int]:
    root = root.expanduser().resolve()
    today = dt.date.today().isoformat()
    selected_mode = mode or detect_vault_mode(root)
    language = detect_vault_language(root)
    checks = health_checks_for_mode(root, selected_mode, language)
    if selected_mode == "shared-core":
        inbox_counts = {}
        missing_bridges = []
    else:
        inbox_counts = count_inbox_files(root, language)
        missing_bridges = project_dirs_without_bridge(root, language)
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

    if selected_mode == "shared-core":
        lines.extend(
            [
                "",
                "## Scope",
                "",
                "This audit covers only manifest-managed shared-core files. Private projects, Inbox, archives, and local extensions are outside this report.",
                "",
                "## Recommended Next Action",
                "",
                "1. If a managed hash differs, review local drift before running `upgrade-core`.",
                "2. Run the vault's own local health check for private working content.",
            ]
        )
    else:
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
        language = detect_vault_language(root)
        report_dir = root / language_target_path(language, AUDIT_REPORT_DIR)
        report_dir.mkdir(parents=True, exist_ok=True)
        today = dt.date.today().isoformat()
        target = report_dir / f"AUDIT-{today}.md"
        if target.exists():
            stamp = dt.datetime.now().strftime("%H%M%S")
            target = report_dir / f"AUDIT-{today}-{stamp}.md"
        target.write_text(report, encoding="utf-8")
        print(f"created {target}")
    return 0
