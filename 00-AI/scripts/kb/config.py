from __future__ import annotations

from pathlib import Path

CORE_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "install.sh",
    "index.md",
    "00-AI/START-HERE.md",
    "00-AI/AGENTS.md",
    "00-AI/governance/README.md",
    "00-AI/governance/startup-contract.md",
    "00-AI/governance/write-back-rules.md",
    "00-AI/governance/review-gates.md",
    "00-AI/governance/maintenance-loop.md",
    "CHANGELOG.md",
    "LICENSE",
    "VERSION",
    "docs/30-second-demo.md",
    "docs/automation.md",
    "docs/legal/content-license.md",
    "docs/migration.md",
    "01-Inbox/README.md",
    "00-AI/pipeline/README.md",
    "00-AI/pipeline/local-material-intake.md",
    "00-AI/pipeline/source-to-knowledge-workflow.md",
    "00-AI/recall/README.md",
    "00-AI/recall/example-recall-chain.md",
    "00-AI/recall/task-to-context-map.md",
    "00-AI/recall/recall-fields.md",
    "10-Projects/PROJECTS-REGISTRY.md",
    "10-Projects/README.md",
    "20-SharedAssets/README.md",
    "20-SharedAssets/01-user-assets/README.md",
    "20-SharedAssets/02-modules/project-lesson-promotion-v1.md",
    "40-ExternalSources/README.md",
    "00-AI/templates/TPL-project-bridge-card.md",
    "00-AI/templates/TPL-task-state-card.md",
    "00-AI/templates/TPL-incident-experience-card.md",
    "00-AI/bases/README.md",
    "00-AI/bases/project-overview.base",
    "00-AI/bases/task-overview.base",
    "00-AI/bases/source-overview.base",
    "00-AI/config/stale-patterns.txt",
    "00-AI/scripts/README.md",
    "00-AI/scripts/kb.py",
    "00-AI/scripts/kb/__init__.py",
]

FULL_INSTALL_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "README.zh-CN.md",
    "install.sh",
    "index.md",
    "CHANGELOG.md",
    "LICENSE",
    "VERSION",
    "00-AI/START-HERE.md",
    "00-AI/AGENTS.md",
    "00-AI/governance",
    "00-AI/pipeline",
    "00-AI/recall",
    "00-AI/templates",
    "00-AI/bases",
    "00-AI/config/stale-patterns.txt",
    "00-AI/scripts/README.md",
    "00-AI/scripts/kb.py",
    "00-AI/scripts/kb",
    "01-Inbox",
    "10-Projects",
    "20-SharedAssets",
    "40-ExternalSources",
    "examples/ai-handoff-demo",
    "examples/claude-code-hooks",
    "examples/filled-example",
    "examples/source-to-knowledge",
    "docs",
]

BAREBONE_INSTALL_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "VERSION",
    "index.md",
    "00-AI/START-HERE.md",
    "00-AI/AGENTS.md",
    "00-AI/governance",
    "00-AI/pipeline/README.md",
    "00-AI/pipeline/local-material-intake.md",
    "00-AI/pipeline/source-to-knowledge-workflow.md",
    "00-AI/recall/README.md",
    "00-AI/recall/example-recall-chain.md",
    "00-AI/recall/recall-fields.md",
    "00-AI/recall/task-to-context-map.md",
    "01-Inbox/README.md",
    "10-Projects/README.md",
    "10-Projects/PROJECTS-REGISTRY.md",
    "20-SharedAssets/README.md",
    "20-SharedAssets/01-user-assets/README.md",
    "20-SharedAssets/02-modules/project-lesson-promotion-v1.md",
    "20-SharedAssets/02-modules/vault-health-checklist-v1.md",
    "20-SharedAssets/02-modules/metadata-minimum-standard-v1.md",
    "40-ExternalSources/README.md",
    "00-AI/templates/TPL-project-bridge-card.md",
    "00-AI/templates/TPL-task-state-card.md",
    "00-AI/templates/TPL-source-analysis-card.md",
    "00-AI/templates/TPL-agent-handoff-card.md",
    "00-AI/templates/TPL-incident-experience-card.md",
    "00-AI/templates/TPL-question-knowledge-experience-asset-card.md",
    "00-AI/config/stale-patterns.txt",
    "00-AI/scripts/kb.py",
    "00-AI/scripts/kb",
]

# Reusable system files that may be managed inside an established working
# vault. This profile deliberately excludes entry pages, Inbox, projects,
# archives, examples, repository documentation, and root-level legal/version
# files so a core upgrade cannot take ownership of private working content.
SHARED_CORE_INSTALL_PATHS = [
    "00-AI/AGENTS.md",
    "00-AI/governance",
    "00-AI/pipeline",
    "00-AI/recall",
    "00-AI/templates",
    "00-AI/bases",
    "00-AI/config",
    "00-AI/scripts/README.md",
    "00-AI/scripts/kb.py",
    "00-AI/scripts/kb",
    "20-SharedAssets/02-modules",
]

LEGACY_STATIC_RENAMES = {
    "20-SharedAssets/02-modules/AI知识库复利维护SOP-v1.md": "20-SharedAssets/02-modules/ai-vault-maintenance-sop-v1.md",
    "20-SharedAssets/02-modules/Codex项目经验资产化机制-v1.md": "20-SharedAssets/02-modules/project-lesson-promotion-v1.md",
    "20-SharedAssets/02-modules/元数据最小标准-v1.md": "20-SharedAssets/02-modules/metadata-minimum-standard-v1.md",
    "20-SharedAssets/02-modules/标签与召回字段设计-v1.md": "20-SharedAssets/02-modules/tags-and-recall-fields-v1.md",
    "20-SharedAssets/02-modules/知识库巡检清单-v1.md": "20-SharedAssets/02-modules/vault-health-checklist-v1.md",
    "20-SharedAssets/04-optional-advanced/跨项目多窗口协作写作规范-v2.1.md": "20-SharedAssets/04-optional-advanced/multi-agent-collaboration-writing-v2.1.md",
    "90-Templates/TPL-Agent交接卡.md": "90-Templates/TPL-agent-handoff-card.md",
    "90-Templates/TPL-Codex项目桥接卡.md": "90-Templates/TPL-project-bridge-card.md",
    "90-Templates/TPL-WebClip-最简模板.md": "90-Templates/TPL-web-clip-minimal.md",
    "90-Templates/TPL-任务状态卡.md": "90-Templates/TPL-task-state-card.md",
    "90-Templates/TPL-资料分析卡.md": "90-Templates/TPL-source-analysis-card.md",
    "90-Templates/TPL-问题事故经验卡.md": "90-Templates/TPL-incident-experience-card.md",
    "90-Templates/TPL-问题知识卡-经验资产卡.md": "90-Templates/TPL-question-knowledge-experience-asset-card.md",
    "90-Templates/TPL-验收记录.md": "90-Templates/TPL-acceptance-record.md",
    "00-AI/templates/TPL-Agent交接卡.md": "00-AI/templates/TPL-agent-handoff-card.md",
    "00-AI/templates/TPL-Codex项目桥接卡.md": "00-AI/templates/TPL-project-bridge-card.md",
    "00-AI/templates/TPL-WebClip-最简模板.md": "00-AI/templates/TPL-web-clip-minimal.md",
    "00-AI/templates/TPL-任务状态卡.md": "00-AI/templates/TPL-task-state-card.md",
    "00-AI/templates/TPL-资料分析卡.md": "00-AI/templates/TPL-source-analysis-card.md",
    "00-AI/templates/TPL-问题事故经验卡.md": "00-AI/templates/TPL-incident-experience-card.md",
    "00-AI/templates/TPL-问题知识卡-经验资产卡.md": "00-AI/templates/TPL-question-knowledge-experience-asset-card.md",
    "00-AI/templates/TPL-验收记录.md": "00-AI/templates/TPL-acceptance-record.md",
}

AI_LAYOUT_RENAMES = {
    "START-HERE.md": "00-AI/START-HERE.md",
    "AGENTS.md": "00-AI/AGENTS.md",
    "00-Agent-Governance": "00-AI/governance",
    "02-Knowledge-Pipeline": "00-AI/pipeline",
    "03-Recall-System": "00-AI/recall",
    "90-Templates": "00-AI/templates",
    "scripts": "00-AI/scripts",
}

AI_LAYOUT_REFERENCE_REPLACEMENTS = [
    ("00-Agent-Governance/", "00-AI/governance/"),
    ("00-Agent-Governance", "00-AI/governance"),
    ("02-Knowledge-Pipeline/", "00-AI/pipeline/"),
    ("02-Knowledge-Pipeline", "00-AI/pipeline"),
    ("03-Recall-System/", "00-AI/recall/"),
    ("03-Recall-System", "00-AI/recall"),
    ("90-Templates/", "00-AI/templates/"),
    ("90-Templates", "00-AI/templates"),
]

SKIP_INSTALL_PARTS = {".git", "__pycache__"}
LANGUAGE_TEMPLATE_ROOT = "00-AI/i18n"
VALID_LANGUAGES = ("en", "zh-CN")
DEFAULT_LANGUAGE = "en"
DEFAULT_INSTALL_MODE = "barebone"
ZH_CN_TARGET_RENAMES = [
    ("00-AI/START-HERE.md", "00-入口/开始这里.md"),
    ("00-AI/AGENTS.md", "90-系统/AI协作规则.md"),
    ("00-AI/governance/maintenance-loop.md", "90-系统/规则/维护循环.md"),
    ("00-AI/governance/review-gates.md", "90-系统/规则/写入审查门槛.md"),
    ("00-AI/governance/startup-contract.md", "90-系统/规则/开工约定.md"),
    ("00-AI/governance/write-back-rules.md", "90-系统/规则/写回规则.md"),
    ("00-AI/governance", "90-系统/规则"),
    ("00-AI/pipeline/local-material-intake.md", "20-资料/处理流程/本机资料进入流程.md"),
    ("00-AI/pipeline/source-to-knowledge-workflow.md", "20-资料/处理流程/资料转知识流程.md"),
    ("00-AI/pipeline", "20-资料/处理流程"),
    ("00-AI/recall/task-to-context-map.md", "90-系统/召回/任务上下文地图.md"),
    ("00-AI/recall/recall-fields.md", "90-系统/召回/召回字段.md"),
    ("00-AI/recall/example-recall-chain.md", "90-系统/召回/示例召回链.md"),
    ("00-AI/recall", "90-系统/召回"),
    ("00-AI/templates/TPL-project-bridge-card.md", "90-系统/模板/TPL-项目桥接卡.md"),
    ("00-AI/templates/TPL-agent-handoff-card.md", "90-系统/模板/TPL-Agent交接卡.md"),
    ("00-AI/templates/TPL-source-analysis-card.md", "90-系统/模板/TPL-资料分析卡.md"),
    ("00-AI/templates/TPL-task-state-card.md", "90-系统/模板/TPL-任务状态卡.md"),
    ("00-AI/templates/TPL-acceptance-record.md", "90-系统/模板/TPL-验收记录.md"),
    ("00-AI/templates/TPL-incident-experience-card.md", "90-系统/模板/TPL-问题事故经验卡.md"),
    (
        "00-AI/templates/TPL-question-knowledge-experience-asset-card.md",
        "90-系统/模板/TPL-问题知识卡-经验资产卡.md",
    ),
    ("00-AI/templates/TPL-web-clip-minimal.md", "90-系统/模板/TPL-WebClip-最简模板.md"),
    ("00-AI/templates", "90-系统/模板"),
    ("00-AI/bases/project-overview.base", "90-系统/视图/项目总览.base"),
    ("00-AI/bases/task-overview.base", "90-系统/视图/任务总览.base"),
    ("00-AI/bases/source-overview.base", "90-系统/视图/资料总览.base"),
    ("00-AI/bases", "90-系统/视图"),
    ("00-AI/config/stale-patterns.txt", "90-系统/配置/过时概念.txt"),
    ("00-AI/config", "90-系统/配置"),
    ("00-AI/scripts", "90-系统/脚本"),
    ("00-AI", "90-系统/AI"),
    ("01-Inbox/agent-handoffs", "01-收件箱/Agent交接"),
    ("01-Inbox/tasks", "01-收件箱/任务"),
    ("01-Inbox/dispatch-cards", "01-收件箱/派工卡"),
    ("01-Inbox/web-clips", "01-收件箱/网页剪藏"),
    ("01-Inbox", "01-收件箱"),
    ("10-Projects/PROJECTS-REGISTRY.md", "10-项目/项目登记表.md"),
    ("10-Projects/01-example-project", "10-项目/01-示例项目"),
    ("10-Projects", "10-项目"),
    ("20-SharedAssets/02-modules/project-lesson-promotion-v1.md", "30-经验资产/02-通用模块/项目经验沉淀机制-v1.md"),
    ("20-SharedAssets/02-modules/vault-health-checklist-v1.md", "30-经验资产/02-通用模块/知识库健康检查清单-v1.md"),
    ("20-SharedAssets/02-modules/ai-vault-maintenance-sop-v1.md", "30-经验资产/02-通用模块/AI知识库维护SOP-v1.md"),
    ("20-SharedAssets/02-modules/metadata-minimum-standard-v1.md", "30-经验资产/02-通用模块/元数据最小标准-v1.md"),
    ("20-SharedAssets/02-modules/tags-and-recall-fields-v1.md", "30-经验资产/02-通用模块/标签与召回字段-v1.md"),
    ("20-SharedAssets/01-user-assets", "30-经验资产/06-本地经验"),
    ("20-SharedAssets/02-modules", "30-经验资产/02-通用模块"),
    ("20-SharedAssets/03-workflows", "30-经验资产/03-工作流"),
    ("20-SharedAssets/04-optional-advanced", "30-经验资产/04-可选进阶"),
    ("20-SharedAssets", "30-经验资产"),
    ("40-ExternalSources/01-samples", "20-资料/01-示例"),
    ("40-ExternalSources", "20-资料"),
    ("index.md", "首页.md"),
]
LANGUAGE_TARGET_RENAMES = {"zh-CN": ZH_CN_TARGET_RENAMES}
ZH_CN_TEXT_REFERENCE_REPLACEMENTS = [
    ("./metadata-minimum-standard-v1.md", "./元数据最小标准-v1.md"),
    ("metadata-minimum-standard-v1", "元数据最小标准-v1"),
    ("./project-lesson-promotion-v1.md", "./项目经验沉淀机制-v1.md"),
    ("project-lesson-promotion-v1", "项目经验沉淀机制-v1"),
]
LANGUAGE_TEXT_REFERENCE_REPLACEMENTS = {"zh-CN": ZH_CN_TEXT_REFERENCE_REPLACEMENTS}
FOLDER_INTAKE_IGNORE_DIRS = {
    ".git",
    ".obsidian",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "target",
}
AUDIT_REPORT_DIR = "20-SharedAssets/05-audit-reports"
MANIFEST_DIR = ".obsidian-ai-workflow-kit"
MANIFEST_FILE = "manifest.json"
ADAPTER_POLICY_FILE = "adoption-policy.json"
MANIFEST_SCHEMA = 1
DEFAULT_STALE_PATTERNS_FILE = "00-AI/config/stale-patterns.txt"
VAULT_STALE_PATTERNS_FILE = f"{MANIFEST_DIR}/stale-patterns.txt"

STATUS_VALUES = {
    "governance": {"draft", "active", "deprecated", "historical"},
    "project": {"active", "waiting", "paused", "blocked", "done", "archived"},
    "external": {"inbox", "filed", "processed", "rejected"},
    "local_task": {"queued", "active", "blocked", "done", "archived"},
    "handoff": {"open", "blocked", "done", "archived"},
    "review": {"pending", "accepted", "deferred", "skipped"},
}

STATUS_TYPE_POLICIES = {
    "project-root": "project",
    "project-readme": "project",
    "project-bridge": "project",
    "codex-project-bridge": "project",
    "project-state": "project",
    "decisions": "project",
    "source-analysis": "external",
    "analysis-card": "external",
    "folder-intake": "external",
    "web-clip": "external",
    "local-task": "local_task",
    "task_card": "local_task",
    "agent-handoff": "handoff",
    "acceptance": "review",
    "acceptance-record": "review",
}

LEGACY_STATUS_MAPS = {
    "project": {
        "open": "active",
        "draft": "waiting",
        "sample": "active",
        "completed": "done",
        "closed": "done",
        "resolved": "done",
    },
    "external": {
        "draft": "inbox",
        "active": "processed",
        "sample": "processed",
        "done": "processed",
        "archived": "filed",
    },
    "local_task": {
        "todo": "queued",
        "pending": "queued",
        "ready": "queued",
        "claimed": "active",
        "doing": "active",
        "review": "active",
        "dev": "active",
        "scoping": "active",
        "completed": "done",
        "closed": "done",
        "resolved": "done",
    },
    "handoff": {"closed": "done", "historical": "archived"},
    "review": {"pass": "accepted", "fail": "deferred", "partial": "deferred"},
}

PROJECT_ENTRY_REQUIRED_FIELDS = {
    "type",
    "updated",
    "status",
    "pillar",
    "project",
    "priority",
    "stage",
    "next_action",
    "last_verified",
}
PROJECT_ENTRY_CURRENT_STATUSES = {"active", "waiting", "paused", "blocked"}
PROJECT_ENTRY_ALL_STATUSES = PROJECT_ENTRY_CURRENT_STATUSES | {"done", "archived"}
PROJECT_PRIORITY_VALUES = {"p0", "p1", "p2", "p3"}
LOCAL_TASK_REQUIRED_FIELDS = {"type", "created", "updated", "status", "project", "priority", "next_action"}
EXTERNAL_BASE_TYPES = {"source-analysis", "analysis-card", "folder-intake", "web-clip"}


def install_paths_for_mode(mode: str) -> list[str]:
    if mode == "full":
        return FULL_INSTALL_PATHS
    if mode == "barebone":
        return BAREBONE_INSTALL_PATHS
    if mode == "shared-core":
        return SHARED_CORE_INSTALL_PATHS
    raise SystemExit("mode must be full, barebone, or shared-core")


def required_paths_for_mode(mode: str, language: str | None = None) -> list[str]:
    selected_language = validate_language(language)
    if mode == "full":
        return [language_target_path(selected_language, path).as_posix() for path in CORE_PATHS]
    if mode == "barebone":
        return [language_target_path(selected_language, path).as_posix() for path in BAREBONE_INSTALL_PATHS]
    if mode == "shared-core":
        return [language_target_path(selected_language, path).as_posix() for path in SHARED_CORE_INSTALL_PATHS]
    raise SystemExit("mode must be full, barebone, or shared-core")


def validate_language(language: str | None) -> str:
    selected = language or DEFAULT_LANGUAGE
    if selected not in VALID_LANGUAGES:
        raise SystemExit(f"language must be one of: {', '.join(VALID_LANGUAGES)}")
    return selected


def language_for_install(args) -> str:
    return validate_language(getattr(args, "language", None))


def language_for_upgrade(args, manifest: dict) -> str:
    selected = getattr(args, "language", None)
    if selected is None:
        selected = manifest.get("language")
    return validate_language(selected)


def language_source_path(source_root, language: str, relative):
    localized = source_root / LANGUAGE_TEMPLATE_ROOT / language / relative
    if localized.exists():
        return localized
    return source_root / relative


def language_target_path(language: str, relative) -> Path:
    selected = validate_language(language)
    rel = Path(relative).as_posix()
    for source, target in LANGUAGE_TARGET_RENAMES.get(selected, []):
        if rel == source:
            return Path(target)
        if rel.startswith(f"{source}/"):
            return Path(f"{target}{rel[len(source):]}")
    return Path(rel)


def localize_text_references(text: str, language: str) -> str:
    selected = validate_language(language)
    replacements = sorted(LANGUAGE_TARGET_RENAMES.get(selected, []), key=lambda pair: len(pair[0]), reverse=True)
    for source, target in replacements:
        text = text.replace(source, target)
    for source, target in LANGUAGE_TEXT_REFERENCE_REPLACEMENTS.get(selected, []):
        text = text.replace(source, target)
    return text
