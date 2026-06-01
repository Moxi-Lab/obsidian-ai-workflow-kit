#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

TARGET="$TMP_DIR/vault"

OBSIDIAN_AI_MEMORY_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --dry-run "$TARGET" >/tmp/obsidian-ai-memory-kit-dry-run.log
test ! -e "$TARGET"

OBSIDIAN_AI_MEMORY_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" "$TARGET" >/tmp/obsidian-ai-memory-kit-install.log
test -f "$TARGET/START-HERE.md"
test -f "$TARGET/scripts/kb.py"
python3 "$TARGET/scripts/kb.py" health-check --vault "$TARGET" >/tmp/obsidian-ai-memory-kit-health.log

printf 'CUSTOM SENTINEL\n' > "$TARGET/START-HERE.md"
OBSIDIAN_AI_MEMORY_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" "$TARGET" >/tmp/obsidian-ai-memory-kit-skip.log
grep -q 'CUSTOM SENTINEL' "$TARGET/START-HERE.md"

OBSIDIAN_AI_MEMORY_KIT_SOURCE="$ROOT" bash "$ROOT/install.sh" --overwrite "$TARGET" >/tmp/obsidian-ai-memory-kit-overwrite.log
! grep -q 'CUSTOM SENTINEL' "$TARGET/START-HERE.md"

rm -f /tmp/obsidian-ai-memory-kit-dry-run.log \
  /tmp/obsidian-ai-memory-kit-install.log \
  /tmp/obsidian-ai-memory-kit-health.log \
  /tmp/obsidian-ai-memory-kit-skip.log \
  /tmp/obsidian-ai-memory-kit-overwrite.log
