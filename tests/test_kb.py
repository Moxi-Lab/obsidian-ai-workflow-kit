import importlib.util
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


class SlugTests(unittest.TestCase):
    def test_make_slug_returns_source_for_empty_input(self):
        self.assertEqual(kb.make_slug("!!!"), "source")

    def test_validate_slug_rejects_uppercase(self):
        with self.assertRaises(SystemExit):
            kb.validate_slug("Bad-Slug")


if __name__ == "__main__":
    unittest.main()
