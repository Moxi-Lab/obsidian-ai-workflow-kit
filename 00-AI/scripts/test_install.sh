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
python3 "$TARGET/00-AI/scripts/kb.py" health-check --vault "$TARGET" >/tmp/obsidian-ai-workflow-kit-health.log
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
test -f "$BAREBONE_TARGET/10-Projects/README.md"
test -f "$BAREBONE_TARGET/00-AI/templates/TPL-project-bridge-card.md"
test -f "$BAREBONE_TARGET/00-AI/scripts/kb.py"
test ! -d "$BAREBONE_TARGET/00-AI/pipeline"
python3 "$BAREBONE_TARGET/00-AI/scripts/kb.py" health-check --vault "$BAREBONE_TARGET" --mode barebone >/tmp/obsidian-ai-workflow-kit-barebone-health.log

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --language zh-CN --mode barebone "$ZH_TARGET" >/tmp/obsidian-ai-workflow-kit-zh.log
grep -q '语言：中文' "$ZH_TARGET/00-AI/START-HERE.md"
python3 - "$ZH_TARGET" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads((Path(sys.argv[1]) / ".obsidian-ai-workflow-kit" / "manifest.json").read_text(encoding="utf-8"))
assert manifest["language"] == "zh-CN"
PY

rm -f /tmp/obsidian-ai-workflow-kit-dry-run.log \
  /tmp/obsidian-ai-workflow-kit-install.log \
  /tmp/obsidian-ai-workflow-kit-health.log \
  /tmp/obsidian-ai-workflow-kit-update-dry-run.log \
  /tmp/obsidian-ai-workflow-kit-skip.log \
  /tmp/obsidian-ai-workflow-kit-overwrite.log \
  /tmp/obsidian-ai-workflow-kit-barebone.log \
  /tmp/obsidian-ai-workflow-kit-barebone-health.log \
  /tmp/obsidian-ai-workflow-kit-zh.log
