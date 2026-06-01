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
        self.assertIn("CONTENT-LICENSE.md", kb.CORE_PATHS)


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
                "90-Templates/TPL-Codex项目桥接卡.md",
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
            self.assertTrue((target / "90-Templates" / "TPL-Codex项目桥接卡.md").exists())
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
    def write_bridge(self, root: Path, slug: str, updated) -> Path:
        project = root / "10-Projects" / slug
        project.mkdir(parents=True)
        updated_line = f"updated: {updated}\n" if updated is not None else ""
        bridge = project / f"CODEX-BRIDGE-{slug}.md"
        bridge.write_text(
            f"""---
type: codex-project-bridge
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


class SlugTests(unittest.TestCase):
    def test_make_slug_returns_source_for_empty_input(self):
        self.assertEqual(kb.make_slug("!!!"), "source")

    def test_validate_slug_rejects_uppercase(self):
        with self.assertRaises(SystemExit):
            kb.validate_slug("Bad-Slug")


if __name__ == "__main__":
    unittest.main()
