import importlib.util
import argparse
import io
import json
import tempfile
import unittest
import zipfile
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
                "LICENSE",
                "VERSION",
                "index.md",
                "00-AI/START-HERE.md",
                "00-AI/AGENTS.md",
                "00-AI/governance",
                "00-AI/pipeline/README.md",
                "00-AI/pipeline/local-material-intake.md",
                "00-AI/recall/README.md",
                "00-AI/recall/task-to-context-map.md",
                "01-Inbox/README.md",
                "10-Projects/README.md",
                "10-Projects/PROJECTS-REGISTRY.md",
                "20-SharedAssets/README.md",
                "20-SharedAssets/02-modules/project-lesson-promotion-v1.md",
                "20-SharedAssets/02-modules/vault-health-checklist-v1.md",
                "20-SharedAssets/02-modules/metadata-minimum-standard-v1.md",
                "40-ExternalSources/README.md",
                "00-AI/templates/TPL-project-bridge-card.md",
                "00-AI/templates/TPL-task-state-card.md",
                "00-AI/templates/TPL-source-analysis-card.md",
                "00-AI/templates/TPL-agent-handoff-card.md",
                "00-AI/config/stale-patterns.txt",
                "00-AI/scripts/kb.py",
                "00-AI/scripts/kb",
            ],
        )

    def test_default_install_mode_is_minimal_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            args = argparse.Namespace(
                target=str(target),
                dry_run=False,
                overwrite=False,
            )

            kb.install_core(args)

            manifest = kb.load_manifest(target)
            self.assertEqual(manifest["mode"], "barebone")
            self.assertTrue((target / "index.md").exists())
            self.assertTrue((target / "00-AI" / "START-HERE.md").exists())
            self.assertFalse((target / "docs").exists())

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
            self.assertTrue((target / "00-AI" / "pipeline" / "README.md").exists())
            self.assertTrue((target / "00-AI" / "recall" / "task-to-context-map.md").exists())
            self.assertTrue((target / "01-Inbox" / "README.md").exists())
            self.assertTrue((target / "10-Projects" / "README.md").exists())
            self.assertTrue((target / "20-SharedAssets" / "README.md").exists())
            self.assertTrue((target / "20-SharedAssets" / "02-modules" / "project-lesson-promotion-v1.md").exists())
            self.assertTrue((target / "20-SharedAssets" / "02-modules" / "vault-health-checklist-v1.md").exists())
            self.assertTrue((target / "20-SharedAssets" / "02-modules" / "metadata-minimum-standard-v1.md").exists())
            self.assertTrue((target / "40-ExternalSources" / "README.md").exists())
            self.assertTrue((target / "00-AI" / "templates" / "TPL-project-bridge-card.md").exists())
            self.assertTrue((target / "00-AI" / "templates" / "TPL-agent-handoff-card.md").exists())
            self.assertTrue((target / "00-AI" / "templates" / "TPL-task-state-card.md").exists())
            self.assertFalse((target / "00-AI" / "templates" / "TPL-acceptance-record.md").exists())
            self.assertTrue((target / "00-AI" / "config" / "stale-patterns.txt").exists())
            self.assertTrue((target / "00-AI" / "scripts" / "kb.py").exists())
            self.assertTrue((target / "00-AI" / "scripts" / "kb" / "__init__.py").exists())
            self.assertFalse((target / "docs").exists())
            self.assertFalse((target / "examples").exists())

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

    def test_health_check_uses_manifest_mode_by_default_for_barebone_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )

            kb.install_core(args)

            health_args = argparse.Namespace(vault=str(target), mode=None)
            self.assertEqual(kb.health_check(health_args), 0)

    def test_audit_report_uses_manifest_mode_by_default_for_barebone_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            args = argparse.Namespace(
                target=str(target),
                mode="barebone",
                dry_run=False,
                overwrite=False,
            )

            kb.install_core(args)

            report, issue_count = kb.build_audit_report(target)
            self.assertEqual(issue_count, 0)
            self.assertNotIn("missing README.md", report)
            self.assertNotIn("missing required path", report)

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

            start_here_path = target / "00-入口" / "开始这里.md"
            start_here = start_here_path.read_text(encoding="utf-8")
            manifest = kb.load_manifest(target)
            self.assertEqual(manifest["language"], "zh-CN")
            self.assertIn("00-入口/开始这里.md", manifest["files"])
            self.assertIn("语言：中文", start_here)
            self.assertIn("00-入口/开始这里.md", start_here)
            self.assertNotIn("Language: English", start_here)
            self.assertNotIn("00-AI", start_here)
            self.assertNotIn("00-智能体", start_here)
            self.assertNotIn("20-SharedAssets", start_here)
            self.assertNotIn("40-ExternalSources", start_here)
            self.assertFalse((target / "00-AI" / "START-HERE.md").exists())
            self.assertTrue((target / "首页.md").exists())
            self.assertTrue((target / "01-收件箱" / "README.md").exists())
            self.assertTrue((target / "10-项目" / "项目登记表.md").exists())
            self.assertTrue((target / "20-资料" / "README.md").exists())
            self.assertTrue((target / "20-资料" / "处理流程" / "README.md").exists())
            self.assertTrue((target / "30-经验资产" / "README.md").exists())
            self.assertTrue((target / "30-经验资产" / "02-通用模块" / "项目经验沉淀机制-v1.md").exists())
            self.assertTrue((target / "30-经验资产" / "02-通用模块" / "知识库健康检查清单-v1.md").exists())
            self.assertTrue((target / "30-经验资产" / "02-通用模块" / "元数据最小标准-v1.md").exists())
            self.assertTrue((target / "90-系统" / "模板" / "TPL-项目桥接卡.md").exists())
            self.assertTrue((target / "90-系统" / "模板" / "TPL-Agent交接卡.md").exists())
            self.assertTrue((target / "90-系统" / "脚本" / "kb.py").exists())
            self.assertFalse((target / "00-智能体").exists())
            self.assertFalse((target / "40-外部资料").exists())

    def test_chinese_barebone_health_check_passes_after_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"

            kb.install_core(self.install_args(target, "zh-CN"))

            health_args = argparse.Namespace(vault=str(target), mode="barebone")
            self.assertEqual(kb.health_check(health_args), 0)

    def test_chinese_start_here_routes_document_organization_to_direct_suggestions(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"

            kb.install_core(self.install_args(target, "zh-CN"))

            start_here = (target / "00-入口" / "开始这里.md").read_text(encoding="utf-8")
            self.assertIn("文档整理与分类建议", start_here)
            self.assertIn("输出整理建议", start_here)
            self.assertIn("不要默认创建映射", start_here)
            self.assertIn("20-资料/处理流程/本机资料进入流程.md", start_here)
            self.assertNotIn("00-AI/START-HERE.md", start_here)

    def test_english_start_here_routes_document_organization_to_direct_suggestions(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"

            kb.install_core(self.install_args(target, "en"))

            start_here = (target / "00-AI" / "START-HERE.md").read_text(encoding="utf-8")
            self.assertIn("Document organization and classification suggestions", start_here)
            self.assertIn("Return organization suggestions", start_here)
            self.assertIn("Do not create a mapping", start_here)

    def test_chinese_new_project_uses_localized_project_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            kb.install_core(self.install_args(target, "zh-CN"))

            kb.new_project(
                argparse.Namespace(
                    slug="demo-project",
                    vault=str(target),
                    name="Demo Project",
                    root=str(Path(tmp) / "demo-project"),
                    dry_run=False,
                )
            )

            project = target / "10-项目" / "demo-project"
            bridge = project / "BRIDGE-demo-project.md"
            self.assertTrue(bridge.exists())
            self.assertFalse((target / "10-Projects" / "demo-project").exists())
            text = bridge.read_text(encoding="utf-8")
            self.assertIn("00-入口/开始这里.md", text)
            self.assertIn("10-项目/demo-project/current-state.md", text)
            self.assertNotIn("00-AI/START-HERE.md", text)

    def test_chinese_folder_intake_uses_localized_source_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            source = Path(tmp) / "demo-materials"
            source.mkdir()
            (source / "example.md").write_text("demo", encoding="utf-8")
            kb.install_core(self.install_args(target, "zh-CN"))

            kb.intake_folder(
                argparse.Namespace(
                    folder=str(source),
                    vault=str(target),
                    title="Demo Materials",
                    project="demo-project",
                    slug=None,
                    extensions=None,
                    max_files=200,
                    include_hidden=False,
                    force=False,
                    dry_run=False,
                )
            )

            card = target / "20-资料" / "02-folder-intakes" / "demo-materials.md"
            self.assertTrue(card.exists())
            self.assertFalse((target / "40-ExternalSources" / "02-folder-intakes").exists())
            self.assertIn("20-资料/处理流程/本机资料进入流程.md", card.read_text(encoding="utf-8"))

    def test_chinese_audit_report_uses_localized_inbox_path_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "vault"
            kb.install_core(self.install_args(target, "zh-CN"))

            report, issue_count = kb.build_audit_report(target)

            self.assertEqual(issue_count, 0)
            self.assertIn("01-收件箱/Agent交接", report)
            self.assertIn("01-收件箱/任务", report)
            self.assertIn("01-收件箱/网页剪藏", report)
            self.assertNotIn("agent-handoffs", report)
            self.assertNotIn("dispatch-cards", report)
            self.assertNotIn("web-clips", report)

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
            start_here = target / "00-入口" / "开始这里.md"
            start_here.write_text("OLD LANGUAGE FILE\n", encoding="utf-8")
            manifest = kb.load_manifest(target)
            manifest["files"]["00-入口/开始这里.md"] = {"sha256": kb.file_sha256(start_here)}
            kb.save_manifest(target, manifest, ROOT, "barebone", False)

            kb.upgrade_core(self.upgrade_args(target))

            text = start_here.read_text(encoding="utf-8")
            self.assertIn("语言：中文", text)
            self.assertNotIn("OLD LANGUAGE FILE", text)


class FirstRunDocumentationTests(unittest.TestCase):
    def test_english_first_run_matches_default_barebone_install(self):
        text = (ROOT / "docs" / "10-minute-first-run.md").read_text(encoding="utf-8")

        self.assertIn("mkdir -p ~/demo-materials", text)
        self.assertIn(
            "python3 ~/obsidian-ai-workflow-test/00-AI/scripts/kb.py health-check "
            "--vault ~/obsidian-ai-workflow-test --mode barebone",
            text,
        )

    def test_chinese_first_run_uses_chinese_install_commands(self):
        text = (ROOT / "docs" / "10-minute-first-run.zh-CN.md").read_text(encoding="utf-8")

        self.assertIn("--language zh-CN --dry-run ~/obsidian-ai-workflow-test", text)
        self.assertIn("--language zh-CN ~/obsidian-ai-workflow-test", text)
        self.assertIn("mkdir -p ~/demo-materials", text)
        self.assertIn("90-系统/脚本/kb.py", text)
        self.assertIn("00-入口/开始这里.md", text)


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
            self.assertIn("project_entry: true", text)
            self.assertIn('pillar: "general"', text)

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


class V09MigrationTests(unittest.TestCase):
    def test_migrate_v09_moves_tasks_maps_status_and_adds_project_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_tasks = root / "01-Inbox" / "dispatch-cards"
            project = root / "10-Projects" / "demo"
            old_tasks.mkdir(parents=True)
            project.mkdir(parents=True)
            (old_tasks / "TASK-demo.md").write_text(
                """---
type: task_card
created: 2026-06-01
updated: 2026-06-01
status: doing
project: Demo
priority: high
next_action: Verify migration
---

# Task
""",
                encoding="utf-8",
            )
            (project / "BRIDGE-demo.md").write_text(
                """---
type: project-bridge
status: active
project: Demo
updated: 2026-06-01
---

# Bridge
""",
                encoding="utf-8",
            )
            (root / "note.md").write_text("See 01-Inbox/dispatch-cards/TASK-demo.md\n", encoding="utf-8")

            kb.migrate_v09(argparse.Namespace(vault=str(root), dry_run=False))

            task = root / "01-Inbox" / "tasks" / "TASK-demo.md"
            self.assertTrue(task.exists())
            self.assertFalse((old_tasks / "TASK-demo.md").exists())
            self.assertFalse(old_tasks.exists())
            task_text = task.read_text(encoding="utf-8")
            self.assertIn("type: local-task", task_text)
            self.assertIn("status: active", task_text)
            bridge_text = (project / "BRIDGE-demo.md").read_text(encoding="utf-8")
            self.assertIn("pillar: general", bridge_text)
            self.assertIn("project_entry: true", bridge_text)
            self.assertIn("01-Inbox/tasks/TASK-demo.md", (root / "note.md").read_text(encoding="utf-8"))

    def test_migrate_v09_refuses_task_overwrite_before_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_tasks = root / "01-Inbox" / "dispatch-cards"
            new_tasks = root / "01-Inbox" / "tasks"
            old_tasks.mkdir(parents=True)
            new_tasks.mkdir(parents=True)
            old = old_tasks / "same.md"
            new = new_tasks / "same.md"
            old.write_text("old\n", encoding="utf-8")
            new.write_text("new\n", encoding="utf-8")

            with self.assertRaises(SystemExit):
                kb.migrate_v09(argparse.Namespace(vault=str(root), dry_run=False))

            self.assertEqual(old.read_text(encoding="utf-8"), "old\n")
            self.assertEqual(new.read_text(encoding="utf-8"), "new\n")


class HealthContractTests(unittest.TestCase):
    def test_wikilink_check_reports_missing_and_ambiguous_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a").mkdir()
            (root / "b").mkdir()
            (root / "a" / "Same.md").write_text("# A\n", encoding="utf-8")
            (root / "b" / "Same.md").write_text("# B\n", encoding="utf-8")
            (root / "note.md").write_text("[[Missing]] and [[Same]]\n", encoding="utf-8")

            errors = kb.check_wikilinks(root)

            self.assertTrue(any("broken wikilink" in error for error in errors))
            self.assertTrue(any("ambiguous wikilink" in error for error in errors))

    def test_typed_status_check_rejects_status_from_another_page_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "project.md").write_text(
                "---\ntype: project-bridge\nstatus: queued\n---\n",
                encoding="utf-8",
            )

            errors = kb.check_typed_statuses(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("unsupported project status", errors[0])

    def test_base_dependency_check_requires_project_entry_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "10-Projects" / "demo"
            project.mkdir(parents=True)
            (project / "BRIDGE-demo.md").write_text(
                "---\ntype: project-bridge\nstatus: active\nproject: Demo\nproject_entry: true\n---\n",
                encoding="utf-8",
            )

            errors = kb.check_base_dependency_metadata(root, "en")

            self.assertTrue(any("pillar" in error and "updated" in error for error in errors))

    def test_base_dependency_check_requires_task_fields_and_source_capture_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks = root / "01-Inbox" / "tasks"
            sources = root / "40-ExternalSources"
            tasks.mkdir(parents=True)
            sources.mkdir(parents=True)
            (tasks / "TASK-demo.md").write_text(
                "---\ntype: local-task\nstatus: queued\n---\n",
                encoding="utf-8",
            )
            (sources / "source.md").write_text(
                "---\ntype: source-analysis\nstatus: inbox\n---\n",
                encoding="utf-8",
            )

            errors = kb.check_base_dependency_metadata(root, "en")

            self.assertTrue(any("local task missing metadata" in error for error in errors))
            self.assertTrue(any("missing captured date" in error for error in errors))


class ReleaseBundleTests(unittest.TestCase):
    def test_build_release_creates_openable_chinese_full_vault(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "dist"

            kb.build_release(
                argparse.Namespace(output=str(output), language="zh-CN", mode="full")
            )

            version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
            archive = output / f"obsidian-ai-workflow-kit-v{version}-zh-CN-full.zip"
            self.assertTrue(archive.exists())
            with zipfile.ZipFile(archive) as bundle:
                names = set(bundle.namelist())
            root = f"obsidian-ai-workflow-kit-v{version}-zh-CN-full"
            self.assertIn(f"{root}/00-入口/开始这里.md", names)
            self.assertIn(f"{root}/90-系统/视图/项目总览.base", names)
            self.assertIn(f"{root}/.obsidian/core-plugins.json", names)
            self.assertIn(f"{root}/.obsidian/community-plugins.json", names)
            with zipfile.ZipFile(archive) as bundle:
                project_base = bundle.read(f"{root}/90-系统/视图/项目总览.base").decode("utf-8")
                task_base = bundle.read(f"{root}/90-系统/视图/任务总览.base").decode("utf-8")
                source_base = bundle.read(f"{root}/90-系统/视图/资料总览.base").decode("utf-8")
            self.assertIn('file.inFolder("10-项目")', project_base)
            self.assertIn('file.inFolder("01-收件箱/任务")', task_base)
            self.assertIn('file.inFolder("20-资料")', source_base)
            self.assertNotIn("10-Projects", project_base)


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
