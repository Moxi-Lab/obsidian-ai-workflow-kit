import importlib.util
import argparse
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("kb", ROOT / "scripts" / "kb.py")
kb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kb)


class CorePathTests(unittest.TestCase):
    def test_health_check_requires_license_files(self):
        self.assertIn("LICENSE", kb.CORE_PATHS)
        self.assertIn("docs/legal/content-license.md", kb.CORE_PATHS)


class InstallModeTests(unittest.TestCase):
    def test_barebone_install_paths_are_minimal(self):
        self.assertEqual(
            kb.install_paths_for_mode("barebone"),
            [
                "START-HERE.md",
                "AGENTS.md",
                "00-Agent-Governance",
                "10-Projects/README.md",
                "10-Projects/PROJECTS-REGISTRY.md",
                "90-Templates/TPL-project-bridge-card.md",
                "scripts/kb.py",
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

            self.assertTrue((target / "START-HERE.md").exists())
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "00-Agent-Governance").is_dir())
            self.assertTrue((target / "10-Projects" / "README.md").exists())
            self.assertTrue((target / "90-Templates" / "TPL-project-bridge-card.md").exists())
            self.assertTrue((target / "scripts" / "kb.py").exists())
            self.assertFalse((target / "02-Knowledge-Pipeline").exists())
            self.assertFalse((target / "03-Recall-System").exists())
            self.assertFalse((target / "docs").exists())

    def test_barebone_install_does_not_overwrite_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            target.mkdir()
            start_here = target / "START-HERE.md"
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
            self.assertIn("START-HERE.md", manifest["files"])
            self.assertIn("scripts/kb.py", manifest["files"])

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

            start_here = target / "START-HERE.md"
            start_here.write_text("OLD KIT CONTENT\n", encoding="utf-8")
            manifest = kb.load_manifest(target)
            manifest["files"]["START-HERE.md"] = {"sha256": kb.file_sha256(start_here)}
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

            start_here = target / "START-HERE.md"
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
            start_here = target / "START-HERE.md"
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


class SlugTests(unittest.TestCase):
    def test_make_slug_returns_source_for_empty_input(self):
        self.assertEqual(kb.make_slug("!!!"), "source")

    def test_validate_slug_rejects_uppercase(self):
        with self.assertRaises(SystemExit):
            kb.validate_slug("Bad-Slug")


if __name__ == "__main__":
    unittest.main()
