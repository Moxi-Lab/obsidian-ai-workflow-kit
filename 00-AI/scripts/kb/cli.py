from __future__ import annotations

import argparse

from .health import audit_vault, health_check, stale_check
from .install import install_core, upgrade_core
from .intake import intake_folder, intake_source
from .migrate import migrate_ai_layout, migrate_codex_names
from .project import new_project

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian AI Workflow Kit helper")
    parser.add_argument("--vault", help="Vault root. Defaults to current directory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    health = subparsers.add_parser("health-check", help="Run repository checks")
    health.add_argument("--vault", help="Vault root. Defaults to current directory.")
    health.add_argument("--mode", choices=["full", "barebone"], default="full", help="Required path set to check")
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

    stale = subparsers.add_parser("stale-check", help="Report stale bridge cards and Inbox pile-up")
    stale.add_argument("--vault", help="Vault root. Defaults to current directory.")
    stale.add_argument("--max-age-days", type=int, default=7, help="Bridge card freshness threshold")
    stale.add_argument("--inbox-threshold", type=int, default=10, help="Inbox files allowed per Inbox type")
    stale.add_argument("--fail-on-findings", action="store_true", help="Exit with 1 when findings exist")
    stale.set_defaults(func=stale_check)

    migrate = subparsers.add_parser("migrate-codex-names", help="Rename legacy Codex-specific files to agent-neutral names")
    migrate.add_argument("--vault", help="Vault root. Defaults to current directory.")
    migrate.add_argument("--dry-run", action="store_true", help="Print actions without renaming files")
    migrate.set_defaults(func=migrate_codex_names)

    migrate_layout = subparsers.add_parser("migrate-ai-layout", help="Move legacy AI system files into 00-AI")
    migrate_layout.add_argument("--vault", help="Vault root. Defaults to current directory.")
    migrate_layout.add_argument("--dry-run", action="store_true", help="Print actions without moving files")
    migrate_layout.set_defaults(func=migrate_ai_layout)

    install = subparsers.add_parser("install-core", help="Install the kit into another Obsidian vault")
    install.add_argument("target", help="Target Obsidian vault directory")
    install.add_argument("--mode", choices=["full", "barebone"], default="full", help="Install full kit or minimal barebone kit")
    install.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    install.add_argument(
        "--allow-protected-adapter-write",
        action="store_true",
        help="Override a local-adapter protection policy. Use only after an explicit manual decision.",
    )
    install.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    install.set_defaults(func=install_core)

    upgrade = subparsers.add_parser("upgrade-core", help="Upgrade managed kit files in an installed vault")
    upgrade.add_argument("target", help="Target Obsidian vault directory")
    upgrade.add_argument("--mode", choices=["full", "barebone"], default="full", help="Upgrade full kit or minimal barebone kit")
    upgrade.add_argument("--overwrite", action="store_true", help="Overwrite modified or unmanaged files")
    upgrade.add_argument("--conflict-copy", action="store_true", help="Write new versions beside conflicted files")
    upgrade.add_argument(
        "--allow-protected-adapter-write",
        action="store_true",
        help="Override a local-adapter protection policy. Use only after an explicit manual decision.",
    )
    upgrade.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    upgrade.set_defaults(func=upgrade_core)

    return parser



def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
