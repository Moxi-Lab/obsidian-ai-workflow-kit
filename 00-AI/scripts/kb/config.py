from __future__ import annotations

CORE_PATHS = [
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
    "20-SharedAssets/02-modules/project-lesson-promotion-v1.md",
    "40-ExternalSources/README.md",
    "00-AI/templates/TPL-project-bridge-card.md",
    "00-AI/templates/TPL-incident-experience-card.md",
    "00-AI/config/stale-patterns.txt",
    "00-AI/scripts/README.md",
    "00-AI/scripts/kb.py",
    "00-AI/scripts/kb/__init__.py",
]

FULL_INSTALL_PATHS = [
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
    "00-AI/START-HERE.md",
    "00-AI/AGENTS.md",
    "00-AI/governance",
    "10-Projects/README.md",
    "10-Projects/PROJECTS-REGISTRY.md",
    "00-AI/templates/TPL-project-bridge-card.md",
    "00-AI/config/stale-patterns.txt",
    "00-AI/scripts/kb.py",
    "00-AI/scripts/kb",
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


def install_paths_for_mode(mode: str) -> list[str]:
    if mode == "full":
        return FULL_INSTALL_PATHS
    if mode == "barebone":
        return BAREBONE_INSTALL_PATHS
    raise SystemExit("mode must be full or barebone")


def required_paths_for_mode(mode: str) -> list[str]:
    if mode == "full":
        return CORE_PATHS
    if mode == "barebone":
        return BAREBONE_INSTALL_PATHS
    raise SystemExit("mode must be full or barebone")
