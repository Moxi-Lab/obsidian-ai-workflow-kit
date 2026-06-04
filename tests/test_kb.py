import importlib.util
import argparse
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("kb_entry", ROOT / "00-AI" / "scripts" / "kb.py")
kb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kb)


class CorePathTests(unittest.TestCase):
    def test_cli_entrypoint_stays_thin_after_module_split(self):
        cli_path = ROOT / "00-AI" / "scripts" / "kb.py"
        line_count = len(cli_path.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(line_count, 120)

    def test_default_stale_patterns_are_configured_outside_python(self):
        patterns = kb.load_stale_patterns(ROOT)
        self.assertIn("KB-MANIFEST", patterns)
        self.assertNotIn("四大主线", patterns)
        self.assertNotIn("01-收件箱", patterns)
        self.assertNotIn("20-共享资产", patterns)

    def test_health_check_requires_license_files(self):
        self.assertIn("LICENSE", kb.CORE_PATHS)
        self.assertIn("docs/legal/content-license.md", kb.CORE_PATHS)

    def test_health_check_uses_single_ai_system_directory(self):
        self.assertIn("00-AI/START-HERE.md", kb.CORE_PATHS)
        self.assertIn("00-AI/AGENTS.md", kb.CORE_PATHS)
        self.assertIn("00-AI/governance/README.md", kb.CORE_PATHS)
        self.assertIn("00-AI/pipeline/local-material-intake.md", kb.CORE_PATHS)
        self.assertIn("00-AI/recall/task-to-context-map.md", kb.CORE_PATHS)
        self.assertIn("00-AI/templates/TPL-project-bridge-card.md", kb.CORE_PATHS)
        self.assertNotIn("START-HERE.md", kb.CORE_PATHS)
        self.assertNotIn("00-Agent-Governance/README.md", kb.CORE_PATHS)


class InstallModeTests(unittest.TestCase):
    def test_barebone_install_paths_are_minimal(self):
        self.assertEqual(
            kb.install_paths_for_mode("barebone"),
            [
                "00-AI/START-HERE.md",
                "00-AI/AGENTS.md",
                "00-AI/governance",
                "10-Projects/README.md",
                "10-Projects/PROJECTS-REGISTRY.md",
                "00-AI/templates/TPL-project-bridge-card.md",
                "00-AI/config/stale-patterns.txt",
                "00-AI/scripts/kb.py",
                "00-AI/scripts/kb",
            ],
        )

    def test_barebone_install_excludes_full_mode_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )

            kb.install_core(args)

            self.assertTrue((target / "00-AI" / "START-HERE.md").exists())
            self.assertTrue((target / "00-AI" / "AGENTS.md").exists())
            self.assertTrue((target / "00-AI" / "governance").is_dir())
            self.assertTrue((target / "10-Projects" / "README.md").exists())
            self.assertTrue((target / "00-AI" / "templates" / "TPL-project-bridge-card.md").exists())
            self.assertTrue((target / "00-AI" / "config" / "stale-patterns.txt").exists())
            self.assertTrue((target / "00-AI" / "scripts" / "kb.py").exists())
            self.assertTrue((target / "00-AI" / "scripts" / "kb" / "__init__.py").exists())
            self.assertFalse((target / "02-Knowledge-Pipeline").exists())
            self.assertFalse((target / "03-Recall-System").exists())
            self.assertFalse((target / "90-Templates").exists())
            self.assertFalse((target / "docs").exists())

    def test_barebone_install_does_not_overwrite_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            target.mkdir()
            start_here = target / "00-AI" / "START-HERE.md"
            start_here.parent.mkdir()
            start_here.write_text("CUSTOM SENTINEL\n", encoding="utf-8")
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )

            kb.install_core(args)

            self.assertEqual(start_here.read_text(encoding="utf-8"), "CUSTOM SENTINEL\n")

    def test_barebone_health_check_allows_optional_full_mode_files_to_be_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )

            kb.install_core(args)

            health_args = argparse.Namespace(vault=str(target), mode="barebone")
            self.assertEqual(kb.health_check(health_args), 0)

    def test_install_core_writes_managed_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )

            kb.install_core(args)

            manifest = kb.load_manifest(target)
            self.assertEqual(manifest["kit"], "obsidian-ai-workflow-kit")
            self.assertEqual(manifest["mode"], "barebone")
            self.assertIn("00-AI/START-HERE.md", manifest["files"])
            self.assertIn("00-AI/scripts/kb.py", manifest["files"])
            self.assertIn("00-AI/scripts/kb/__init__.py", manifest["files"])
            self.assertIn("00-AI/config/stale-patterns.txt", manifest["files"])

    def test_install_core_refuses_protected_local_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            policy_dir = target / ".obsidian-ai-workflow-kit"
            policy_dir.mkdir(parents=True)
            (policy_dir / "adoption-policy.json").write_text(
                json.dumps({"mode": "local-adapter", "allow_public_kit_writes": False}),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
                allow_protected_adapter_write=False,
            )

            with self.assertRaises(SystemExit):
                kb.install_core(args)

            self.assertFalse((target / "00-AI" / "START-HERE.md").exists())

    def test_install_core_allows_protected_local_adapter_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            policy_dir = target / ".obsidian-ai-workflow-kit"
            policy_dir.mkdir(parents=True)
            (policy_dir / "adoption-policy.json").write_text(
                json.dumps({"mode": "local-adapter", "allow_public_kit_writes": False}),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=True,
                overwrite=False,
                allow_protected_adapter_write=False,
            )

            self.assertEqual(kb.install_core(args), 0)
            self.assertFalse((target / "00-AI" / "START-HERE.md").exists())

    def test_upgrade_core_updates_unmodified_managed_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            install_args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )
            kb.install_core(install_args)

            start_here = target / "00-AI" / "START-HERE.md"
            start_here.write_text("OLD KIT CONTENT\n", encoding="utf-8")
            manifest = kb.load_manifest(target)
            manifest["files"]["00-AI/START-HERE.md"] = {"sha256": kb.file_sha256(start_here)}
            kb.save_manifest(target, manifest, kb.ROOT if hasattr(kb, "ROOT") else Path(__file__).resolve().parents[1], "barebone", False)

            upgrade_args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
                conflict_copy=False,
            )
            kb.upgrade_core(upgrade_args)

            self.assertNotEqual(start_here.read_text(encoding="utf-8"), "OLD KIT CONTENT\n")
            self.assertIn("# START HERE", start_here.read_text(encoding="utf-8"))

    def test_upgrade_core_skips_modified_managed_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            install_args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )
            kb.install_core(install_args)

            start_here = target / "00-AI" / "START-HERE.md"
            start_here.write_text("USER CUSTOM CONTENT\n", encoding="utf-8")
            upgrade_args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
                conflict_copy=False,
            )

            kb.upgrade_core(upgrade_args)

            self.assertEqual(start_here.read_text(encoding="utf-8"), "USER CUSTOM CONTENT\n")

    def test_upgrade_core_skips_unmanaged_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            target.mkdir()
            start_here = target / "00-AI" / "START-HERE.md"
            start_here.parent.mkdir(parents=True)
            start_here.write_text("UNMANAGED CONTENT\n", encoding="utf-8")
            upgrade_args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
                conflict_copy=False,
            )

            kb.upgrade_core(upgrade_args)

            self.assertEqual(start_here.read_text(encoding="utf-8"), "UNMANAGED CONTENT\n")

    def test_upgrade_core_refuses_protected_local_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            policy_dir = target / ".obsidian-ai-workflow-kit"
            policy_dir.mkdir(parents=True)
            (policy_dir / "adoption-policy.json").write_text(
                json.dumps({"mode": "local-adapter", "allow_public_kit_writes": False}),
                encoding="utf-8",
            )
            upgrade_args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
                conflict_copy=False,
                allow_protected_adapter_write=False,
            )

            with self.assertRaises(SystemExit):
                kb.upgrade_core(upgrade_args)

            self.assertFalse((target / "00-AI" / "START-HERE.md").exists())

    def test_migrate_legacy_ai_layout_moves_files_and_updates_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "00-Agent-Governance").mkdir()
            (root / "02-Knowledge-Pipeline").mkdir()
            (root / "03-Recall-System").mkdir()
            (root / "90-Templates").mkdir()
            (root / "scripts").mkdir()
            (root / "START-HERE.md").write_text("read 00-Agent-Governance/README.md", encoding="utf-8")
            (root / "AGENTS.md").write_text("use 90-Templates/TPL-project-bridge-card.md", encoding="utf-8")
            (root / "00-Agent-Governance" / "README.md").write_text("governance", encoding="utf-8")
            (root / "02-Knowledge-Pipeline" / "local-material-intake.md").write_text("pipeline", encoding="utf-8")
            (root / "03-Recall-System" / "task-to-context-map.md").write_text("recall", encoding="utf-8")
            (root / "90-Templates" / "TPL-project-bridge-card.md").write_text("template", encoding="utf-8")
            (root / "scripts" / "kb.py").write_text("script", encoding="utf-8")
            (root / "note.md").write_text(
                "START-HERE.md 02-Knowledge-Pipeline/local-material-intake.md scripts/kb.py",
                encoding="utf-8",
            )
            args = argparse.Namespace(vault=str(root), dry_run=False)

            kb.migrate_ai_layout(args)

            self.assertTrue((root / "00-AI" / "START-HERE.md").exists())
            self.assertTrue((root / "00-AI" / "AGENTS.md").exists())
            self.assertTrue((root / "00-AI" / "governance" / "README.md").exists())
            self.assertTrue((root / "00-AI" / "pipeline" / "local-material-intake.md").exists())
            self.assertTrue((root / "00-AI" / "recall" / "task-to-context-map.md").exists())
            self.assertTrue((root / "00-AI" / "templates" / "TPL-project-bridge-card.md").exists())
            self.assertTrue((root / "00-AI" / "scripts" / "kb.py").exists())
            self.assertFalse((root / "START-HERE.md").exists())
            self.assertFalse((root / "00-Agent-Governance").exists())
            text = (root / "note.md").read_text(encoding="utf-8")
            self.assertIn("00-AI/START-HERE.md", text)
            self.assertIn("00-AI/pipeline/local-material-intake.md", text)
            self.assertIn("00-AI/scripts/kb.py", text)


class InstallLanguageTests(unittest.TestCase):
    def install_args(self, target: Path, language, dry_run: bool = False):
        return argparse.Namespace(
            target=str(target),
            mode="barebone",
            language=language,
            dry_run=dry_run,
            overwrite=False,
            allow_protected_adapter_write=False,
        )

    def upgrade_args(self, target: Path, language=None):
        return argparse.Namespace(
            target=str(target),
            mode="barebone",
            language=language,
            dry_run=False,
            overwrite=False,
            conflict_copy=False,
            allow_protected_adapter_write=False,
        )

    def test_install_core_writes_selected_chinese_language_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"

            kb.install_core(self.install_args(target, "zh-CN"))

            start_here = (target / "00-AI" / "START-HERE.md").read_text(encoding="utf-8")
            manifest = kb.load_manifest(target)
            self.assertEqual(manifest["language"], "zh-CN")
            self.assertIn("语言：中文", start_here)
            self.assertNotIn("Language: English", start_here)

    def test_install_core_writes_selected_english_language_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"

            kb.install_core(self.install_args(target, "en"))

            start_here = (target / "00-AI" / "START-HERE.md").read_text(encoding="utf-8")
            manifest = kb.load_manifest(target)
            self.assertEqual(manifest["language"], "en")
            self.assertIn("Language: English", start_here)
            self.assertNotIn("语言：中文", start_here)

    def test_install_core_dry_run_prints_selected_language(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            output = io.StringIO()

            with redirect_stdout(output):
                kb.install_core(self.install_args(target, "zh-CN", dry_run=True))

            self.assertIn("language: zh-CN", output.getvalue())
            self.assertFalse(target.exists())

    def test_install_core_rejects_unknown_language(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"

            with self.assertRaises(SystemExit):
                kb.install_core(self.install_args(target, "fr"))

            self.assertFalse(target.exists())

    def test_upgrade_core_reuses_manifest_language_when_omitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            kb.install_core(self.install_args(target, "zh-CN"))
            start_here = target / "00-AI" / "START-HERE.md"
            start_here.write_text("OLD LANGUAGE FILE\n", encoding="utf-8")
            manifest = kb.load_manifest(target)
            manifest["files"]["00-AI/START-HERE.md"] = {"sha256": kb.file_sha256(start_here)}
            kb.save_manifest(target, manifest, ROOT, "barebone", False)

            kb.upgrade_core(self.upgrade_args(target))

            text = start_here.read_text(encoding="utf-8")
            self.assertIn("语言：中文", text)
            self.assertNotIn("OLD LANGUAGE FILE", text)


class ProjectBridgeNamingTests(unittest.TestCase):
    def test_new_project_uses_agent_neutral_bridge_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = argparse.Namespace(
                slug="demo",
                vault=tmp,
                name="Demo",
                root=None,
                dry_run=False,
            )

            kb.new_project(args)

            project = Path(tmp) / "10-Projects" / "demo"
            self.assertTrue((project / "BRIDGE-demo.md").exists())
            self.assertFalse((project / "CODEX-BRIDGE-demo.md").exists())
            text = (project / "BRIDGE-demo.md").read_text(encoding="utf-8")
            self.assertIn("type: project-bridge", text)

    def test_project_dirs_without_bridge_accepts_new_and_legacy_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            new_project = root / "10-Projects" / "new"
            legacy_project = root / "10-Projects" / "legacy"
            missing_project = root / "10-Projects" / "missing"
            new_project.mkdir(parents=True)
            legacy_project.mkdir(parents=True)
            missing_project.mkdir(parents=True)
            (new_project / "BRIDGE-new.md").write_text("---\nupdated: 2026-06-01\n---\n", encoding="utf-8")
            (legacy_project / "CODEX-BRIDGE-legacy.md").write_text("---\nupdated: 2026-06-01\n---\n", encoding="utf-8")

            self.assertEqual(kb.project_dirs_without_bridge(root), ["missing"])


class CodexNameMigrationTests(unittest.TestCase):
    def test_migrate_codex_names_renames_files_and_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "10-Projects" / "demo"
            template_dir = root / "90-Templates"
            module_dir = root / "20-SharedAssets" / "02-modules"
            project.mkdir(parents=True)
            template_dir.mkdir(parents=True)
            module_dir.mkdir(parents=True)
            (project / "CODEX-BRIDGE-demo.md").write_text("bridge", encoding="utf-8")
            (template_dir / "TPL-Codex项目桥接卡.md").write_text("template", encoding="utf-8")
            (module_dir / "Codex项目经验资产化机制-v1.md").write_text("lesson", encoding="utf-8")
            (root / "note.md").write_text(
                "See 10-Projects/demo/CODEX-BRIDGE-demo.md, "
                "90-Templates/TPL-Codex项目桥接卡.md and "
                "20-SharedAssets/02-modules/Codex项目经验资产化机制-v1.md",
                encoding="utf-8",
            )
            args = argparse.Namespace(vault=str(root), dry_run=False)

            kb.migrate_codex_names(args)

            self.assertFalse((project / "CODEX-BRIDGE-demo.md").exists())
            self.assertTrue((project / "BRIDGE-demo.md").exists())
            self.assertTrue((template_dir / "TPL-project-bridge-card.md").exists())
            self.assertTrue((module_dir / "project-lesson-promotion-v1.md").exists())
            text = (root / "note.md").read_text(encoding="utf-8")
            self.assertIn("10-Projects/demo/BRIDGE-demo.md", text)
            self.assertIn("90-Templates/TPL-project-bridge-card.md", text)
            self.assertIn("20-SharedAssets/02-modules/project-lesson-promotion-v1.md", text)


class FolderIntakeTests(unittest.TestCase):
    def test_collect_folder_files_skips_hidden_and_tool_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes").mkdir()
            (root / ".hidden").mkdir()
            (root / "node_modules" / "pkg").mkdir(parents=True)
            (root / "notes" / "a.md").write_text("alpha", encoding="utf-8")
            (root / ".hidden" / "secret.md").write_text("secret", encoding="utf-8")
            (root / "node_modules" / "pkg" / "index.js").write_text("pkg", encoding="utf-8")

            listed, stats = kb.collect_folder_files(
                root,
                include_hidden=False,
                extensions=None,
                max_files=10,
            )

        self.assertEqual([path.name for path in listed], ["a.md"])
        self.assertEqual(stats["skipped_hidden"], 1)
        self.assertEqual(stats["skipped_ignored_dirs"], 1)


class StaleCheckTests(unittest.TestCase):
    def write_bridge(self, root: Path, slug: str, updated, legacy: bool = False) -> Path:
        project = root / "10-Projects" / slug
        project.mkdir(parents=True)
        updated_line = f"updated: {updated}\n" if updated is not None else ""
        prefix = "CODEX-BRIDGE" if legacy else "BRIDGE"
        bridge = project / f"{prefix}-{slug}.md"
        bridge.write_text(
            f"""---
type: project-bridge
status: active
{updated_line}---

# Bridge
""",
            encoding="utf-8",
        )
        return bridge

    def test_finds_bridge_cards_older_than_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_bridge(root, "old-project", "2026-05-20")
            self.write_bridge(root, "fresh-project", "2026-05-31")

            report, count = kb.build_stale_report(
                root,
                max_age_days=7,
                inbox_threshold=10,
                today=kb.dt.date(2026, 6, 1),
            )

            self.assertEqual(count, 1)
            self.assertIn("old-project", report)
            self.assertNotIn("fresh-project", report)

    def test_flags_bridge_cards_without_updated_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_bridge(root, "missing-date", None)

            report, count = kb.build_stale_report(
                root,
                max_age_days=7,
                inbox_threshold=10,
                today=kb.dt.date(2026, 6, 1),
            )

            self.assertEqual(count, 1)
            self.assertIn("missing updated date", report)

    def test_stale_check_accepts_legacy_codex_bridge_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_bridge(root, "legacy-project", "2026-05-20", legacy=True)

            report, count = kb.build_stale_report(
                root,
                max_age_days=7,
                inbox_threshold=10,
                today=kb.dt.date(2026, 6, 1),
            )

            self.assertEqual(count, 1)
            self.assertIn("CODEX-BRIDGE-legacy-project.md", report)

    def test_reports_inbox_when_file_count_exceeds_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inbox = root / "01-Inbox" / "agent-handoffs"
            inbox.mkdir(parents=True)
            (inbox / "a.md").write_text("a", encoding="utf-8")
            (inbox / "b.md").write_text("b", encoding="utf-8")

            report, count = kb.build_stale_report(
                root,
                max_age_days=7,
                inbox_threshold=1,
                today=kb.dt.date(2026, 6, 1),
            )

            self.assertEqual(count, 1)
            self.assertIn("agent-handoffs", report)
            self.assertIn("2 files", report)

    def test_recommendations_name_files_to_update_for_stale_bridge(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_bridge(root, "old-project", "2026-05-20")

            report, _count = kb.build_stale_report(
                root,
                max_age_days=7,
                inbox_threshold=10,
                today=kb.dt.date(2026, 6, 1),
            )

            self.assertIn("updated` field", report)
            self.assertIn("current state", report)
            self.assertIn("recent decisions", report)
            self.assertIn("next startup action", report)

    def test_stale_patterns_are_loaded_from_kit_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_dir = root / "00-AI" / "config"
            config_dir.mkdir(parents=True)
            (config_dir / "stale-patterns.txt").write_text("private-marker\n", encoding="utf-8")
            (root / "note.md").write_text("This has private-marker.\n", encoding="utf-8")

            errors = kb.check_stale_patterns(root)

            self.assertEqual(errors, ["stale concept in note.md: private-marker"])

    def test_vault_stale_patterns_override_kit_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_dir = root / "00-AI" / "config"
            config_dir.mkdir(parents=True)
            (config_dir / "stale-patterns.txt").write_text("default-marker\n", encoding="utf-8")
            override_dir = root / ".obsidian-ai-workflow-kit"
            override_dir.mkdir()
            (override_dir / "stale-patterns.txt").write_text("custom-marker\n", encoding="utf-8")
            (root / "note.md").write_text("default-marker custom-marker\n", encoding="utf-8")

            errors = kb.check_stale_patterns(root)

            self.assertEqual(errors, ["stale concept in note.md: custom-marker"])


class SlugTests(unittest.TestCase):
    def test_make_slug_returns_source_for_empty_input(self):
        self.assertEqual(kb.make_slug("!!!"), "source")

    def test_validate_slug_rejects_uppercase(self):
        with self.assertRaises(SystemExit):
            kb.validate_slug("Bad-Slug")


if __name__ == "__main__":
    unittest.main()
