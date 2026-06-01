#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

TARGET="$TMP_DIR/vault"
BAREBONE_TARGET="$TMP_DIR/barebone-vault"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --dry-run "$TARGET" >/tmp/obsidian-ai-workflow-kit-dry-run.log
test ! -e "$TARGET"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" "$TARGET" >/tmp/obsidian-ai-workflow-kit-install.log
test -f "$TARGET/START-HERE.md"
test -f "$TARGET/scripts/kb.py"
python3 "$TARGET/scripts/kb.py" health-check --vault "$TARGET" >/tmp/obsidian-ai-workflow-kit-health.log

printf 'CUSTOM SENTINEL\n' > "$TARGET/START-HERE.md"
OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" "$TARGET" >/tmp/obsidian-ai-workflow-kit-skip.log
grep -q 'CUSTOM SENTINEL' "$TARGET/START-HERE.md"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --overwrite "$TARGET" >/tmp/obsidian-ai-workflow-kit-overwrite.log
! grep -q 'CUSTOM SENTINEL' "$TARGET/START-HERE.md"

OBSIDIAN_AI_WORKFLOW_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --mode barebone "$BAREBONE_TARGET" >/tmp/obsidian-ai-workflow-kit-barebone.log
test -f "$BAREBONE_TARGET/START-HERE.md"
test -f "$BAREBONE_TARGET/AGENTS.md"
test -d "$BAREBONE_TARGET/00-Agent-Governance"
test -f "$BAREBONE_TARGET/10-Projects/README.md"
test -f "$BAREBONE_TARGET/90-Templates/TPL-Codex项目桥接卡.md"
test -f "$BAREBONE_TARGET/scripts/kb.py"
test ! -d "$BAREBONE_TARGET/02-Knowledge-Pipeline"
python3 "$BAREBONE_TARGET/scripts/kb.py" health-check --vault "$BAREBONE_TARGET" --mode barebone >/tmp/obsidian-ai-workflow-kit-barebone-health.log

rm -f /tmp/obsidian-ai-workflow-kit-dry-run.log \
  /tmp/obsidian-ai-workflow-kit-install.log \
  /tmp/obsidian-ai-workflow-kit-health.log \
  /tmp/obsidian-ai-workflow-kit-skip.log \
  /tmp/obsidian-ai-workflow-kit-overwrite.log \
  /tmp/obsidian-ai-workflow-kit-barebone.log \
  /tmp/obsidian-ai-workflow-kit-barebone-health.log
