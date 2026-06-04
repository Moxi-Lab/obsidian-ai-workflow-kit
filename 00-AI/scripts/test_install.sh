#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

TARGET="$TMP_DIR/vault"
BAREBONE_TARGET="$TMP_DIR/barebone-vault"
ZH_TARGET="$TMP_DIR/zh-vault"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --dry-run "$TARGET" >/tmp/obsidian-ai-workflow-kit-dry-run.log
grep -q "language: en" /tmp/obsidian-ai-workflow-kit-dry-run.log
test ! -e "$TARGET"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" "$TARGET" >/tmp/obsidian-ai-workflow-kit-install.log
test -f "$TARGET/00-AI/START-HERE.md"
test -f "$TARGET/00-AI/scripts/kb.py"
test -f "$TARGET/.obsidian-ai-workflow-kit/manifest.json"
python3 "$TARGET/00-AI/scripts/kb.py" health-check --vault "$TARGET" --mode barebone >/tmp/obsidian-ai-workflow-kit-health.log
OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --update --dry-run "$TARGET" >/tmp/obsidian-ai-workflow-kit-update-dry-run.log
grep -q "would upgrade core files" /tmp/obsidian-ai-workflow-kit-update-dry-run.log

printf 'CUSTOM SENTINEL\n' > "$TARGET/00-AI/START-HERE.md"
OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" "$TARGET" >/tmp/obsidian-ai-workflow-kit-skip.log
grep -q 'CUSTOM SENTINEL' "$TARGET/00-AI/START-HERE.md"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --overwrite "$TARGET" >/tmp/obsidian-ai-workflow-kit-overwrite.log
! grep -q 'CUSTOM SENTINEL' "$TARGET/00-AI/START-HERE.md"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --mode barebone "$BAREBONE_TARGET" >/tmp/obsidian-ai-workflow-kit-barebone.log
test -f "$BAREBONE_TARGET/00-AI/START-HERE.md"
test -f "$BAREBONE_TARGET/00-AI/AGENTS.md"
test -d "$BAREBONE_TARGET/00-AI/governance"
test -f "$BAREBONE_TARGET/00-AI/pipeline/README.md"
test -f "$BAREBONE_TARGET/00-AI/recall/task-to-context-map.md"
test -f "$BAREBONE_TARGET/01-Inbox/README.md"
test -f "$BAREBONE_TARGET/10-Projects/README.md"
test -f "$BAREBONE_TARGET/20-SharedAssets/README.md"
test -f "$BAREBONE_TARGET/20-SharedAssets/02-modules/project-lesson-promotion-v1.md"
test -f "$BAREBONE_TARGET/20-SharedAssets/02-modules/vault-health-checklist-v1.md"
test -f "$BAREBONE_TARGET/20-SharedAssets/02-modules/metadata-minimum-standard-v1.md"
test -f "$BAREBONE_TARGET/40-ExternalSources/README.md"
test -f "$BAREBONE_TARGET/00-AI/templates/TPL-project-bridge-card.md"
test -f "$BAREBONE_TARGET/00-AI/scripts/kb.py"
test ! -d "$BAREBONE_TARGET/docs"
test ! -d "$BAREBONE_TARGET/examples"
python3 "$BAREBONE_TARGET/00-AI/scripts/kb.py" health-check --vault "$BAREBONE_TARGET" --mode barebone >/tmp/obsidian-ai-workflow-kit-barebone-health.log

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --language zh-CN "$ZH_TARGET" >/tmp/obsidian-ai-workflow-kit-zh.log
grep -q '语言：中文' "$ZH_TARGET/00-入口/开始这里.md"
grep -q '00-入口/开始这里.md' "$ZH_TARGET/00-入口/开始这里.md"
test ! -e "$ZH_TARGET/00-AI/START-HERE.md"
test -f "$ZH_TARGET/10-项目/项目登记表.md"
test -f "$ZH_TARGET/20-资料/README.md"
test -f "$ZH_TARGET/20-资料/处理流程/README.md"
test -f "$ZH_TARGET/30-经验资产/README.md"
test -f "$ZH_TARGET/30-经验资产/02-通用模块/项目经验沉淀机制-v1.md"
test -f "$ZH_TARGET/30-经验资产/02-通用模块/知识库健康检查清单-v1.md"
test -f "$ZH_TARGET/30-经验资产/02-通用模块/元数据最小标准-v1.md"
test -f "$ZH_TARGET/90-系统/模板/TPL-项目桥接卡.md"
test -f "$ZH_TARGET/90-系统/召回/任务上下文地图.md"
test -f "$ZH_TARGET/90-系统/脚本/kb.py"
test ! -e "$ZH_TARGET/00-智能体"
test ! -e "$ZH_TARGET/40-外部资料"
python3 "$ZH_TARGET/90-系统/脚本/kb.py" health-check --vault "$ZH_TARGET" --mode barebone >/tmp/obsidian-ai-workflow-kit-zh-health.log
python3 - "$ZH_TARGET" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads((Path(sys.argv[1]) / ".obsidian-ai-workflow-kit" / "manifest.json").read_text(encoding="utf-8"))
assert manifest["language"] == "zh-CN"
assert "00-入口/开始这里.md" in manifest["files"]
PY

rm -f /tmp/obsidian-ai-workflow-kit-dry-run.log \
  /tmp/obsidian-ai-workflow-kit-install.log \
  /tmp/obsidian-ai-workflow-kit-health.log \
  /tmp/obsidian-ai-workflow-kit-update-dry-run.log \
  /tmp/obsidian-ai-workflow-kit-skip.log \
  /tmp/obsidian-ai-workflow-kit-overwrite.log \
  /tmp/obsidian-ai-workflow-kit-barebone.log \
  /tmp/obsidian-ai-workflow-kit-barebone-health.log \
  /tmp/obsidian-ai-workflow-kit-zh.log \
  /tmp/obsidian-ai-workflow-kit-zh-health.log
