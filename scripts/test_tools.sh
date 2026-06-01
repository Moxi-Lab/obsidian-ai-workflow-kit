#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

VAULT="$TMP_DIR/vault"
MATERIALS="$TMP_DIR/materials"

python3 "$ROOT/scripts/kb.py" install-core "$VAULT" >/dev/null

mkdir -p "$MATERIALS/notes" "$MATERIALS/.hidden" "$MATERIALS/node_modules/pkg"
printf 'alpha\n' > "$MATERIALS/notes/a.md"
printf 'beta\n' > "$MATERIALS/notes/b.txt"
printf 'gamma\n' > "$MATERIALS/notes/c.pdf"
printf 'hidden\n' > "$MATERIALS/.hidden/secret.md"
printf 'package\n' > "$MATERIALS/node_modules/pkg/index.js"

python3 "$VAULT/scripts/kb.py" intake-folder "$MATERIALS" \
  --vault "$VAULT" \
  --title "Research Dump" \
  --project demo \
  --max-files 2 >/tmp/kb-intake-folder.log

MANIFEST="$VAULT/40-ExternalSources/02-folder-intakes/research-dump.md"
test -f "$MANIFEST"
grep -q "type: folder-intake" "$MANIFEST"
grep -q "source_folder:" "$MANIFEST"
grep -q "notes/a.md" "$MANIFEST"
grep -q "notes/b.txt" "$MANIFEST"
grep -q "omitted_count:" "$MANIFEST"
grep -q "Original files remain in place" "$MANIFEST"
test -f "$MATERIALS/notes/a.md"
! grep -q ".hidden/secret.md" "$MANIFEST"
! grep -q "node_modules/pkg/index.js" "$MANIFEST"

python3 "$VAULT/scripts/kb.py" intake-folder "$MATERIALS" \
  --vault "$VAULT" \
  --slug dry-run-check \
  --dry-run >/tmp/kb-intake-folder-dry-run.log
test ! -f "$VAULT/40-ExternalSources/02-folder-intakes/dry-run-check.md"

mkdir -p "$VAULT/10-Projects/no-bridge" "$VAULT/01-Inbox/agent-handoffs"
printf 'handoff\n' > "$VAULT/01-Inbox/agent-handoffs/stale.md"

python3 "$VAULT/scripts/kb.py" audit-vault --vault "$VAULT" >/tmp/kb-audit.log
grep -q "Inbox files" /tmp/kb-audit.log
grep -q "Project directories without bridge" /tmp/kb-audit.log
grep -q "no-bridge" /tmp/kb-audit.log
test ! -d "$VAULT/20-SharedAssets/05-audit-reports"

python3 "$VAULT/scripts/kb.py" audit-vault --vault "$VAULT" --write-report >/tmp/kb-audit-write.log
find "$VAULT/20-SharedAssets/05-audit-reports" -name 'AUDIT-*.md' -type f | grep -q .

rm -f /tmp/kb-intake-folder.log \
  /tmp/kb-intake-folder-dry-run.log \
  /tmp/kb-audit.log \
  /tmp/kb-audit-write.log
