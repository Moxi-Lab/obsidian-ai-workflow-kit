#!/usr/bin/env bash
set -euo pipefail

REPO="Moxi-Lab/obsidian-ai-workflow-kit"
BRANCH="${OBSIDIAN_AI_WORKFLOW_KIT_BRANCH:-main}"
ARCHIVE_URL="${OBSIDIAN_AI_WORKFLOW_KIT_ARCHIVE_URL:-https://github.com/${REPO}/archive/refs/heads/${BRANCH}.tar.gz}"
SOURCE="${OBSIDIAN_AI_WORKFLOW_KIT_SOURCE:-}"
DRY_RUN=0
OVERWRITE=0
UPDATE=0
ALLOW_PROTECTED_ADAPTER_WRITE=0
MODE="full"
LANGUAGE="en"
TARGET=""
TMP_DIR=""

usage() {
  cat <<'USAGE'
Install Obsidian AI Workflow Kit into an existing Obsidian vault.

Usage:
  bash install.sh [--dry-run] [--overwrite] [--update] [--allow-protected-adapter-write] [--mode full|barebone] [--language en|zh-CN] [--branch main] [--source /path/to/repo] <vault-path>

Examples:
  bash install.sh --dry-run "/path/to/your-vault"
  bash install.sh "/path/to/your-vault"
  bash install.sh --language zh-CN "/path/to/your-vault"
  bash install.sh --mode barebone "/path/to/your-vault"
  bash install.sh --update --mode barebone --dry-run "/path/to/your-vault"
  bash install.sh --update --mode barebone "/path/to/your-vault"

Remote one-line form:
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --dry-run "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone --dry-run "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone "/path/to/your-vault"

Default behavior:
  - Creates missing files and directories.
  - Skips existing files.
  - Does not overwrite unless --overwrite is passed.
  - In --update mode, only managed and unmodified kit files are updated.
  - Refuses to write into vaults protected by .obsidian-ai-workflow-kit/adoption-policy.json unless --allow-protected-adapter-write is passed.
  - Uses --mode full unless --mode barebone is passed.
  - Uses --language en unless --language zh-CN is passed.
USAGE
}

cleanup() {
  if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --overwrite)
      OVERWRITE=1
      shift
      ;;
    --update)
      UPDATE=1
      shift
      ;;
    --allow-protected-adapter-write)
      ALLOW_PROTECTED_ADAPTER_WRITE=1
      shift
      ;;
    --mode)
      if [[ $# -lt 2 ]]; then
        echo "missing value for --mode" >&2
        exit 2
      fi
      if [[ "$2" != "full" && "$2" != "barebone" ]]; then
        echo "mode must be full or barebone" >&2
        exit 2
      fi
      MODE="$2"
      shift 2
      ;;
    --language)
      if [[ $# -lt 2 ]]; then
        echo "missing value for --language" >&2
        exit 2
      fi
      if [[ "$2" != "en" && "$2" != "zh-CN" ]]; then
        echo "language must be en or zh-CN" >&2
        exit 2
      fi
      LANGUAGE="$2"
      shift 2
      ;;
    --branch)
      if [[ $# -lt 2 ]]; then
        echo "missing value for --branch" >&2
        exit 2
      fi
      BRANCH="$2"
      ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.tar.gz"
      shift 2
      ;;
    --source)
      if [[ $# -lt 2 ]]; then
        echo "missing value for --source" >&2
        exit 2
      fi
      SOURCE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -n "$TARGET" ]]; then
        echo "only one vault path is allowed" >&2
        exit 2
      fi
      TARGET="$1"
      shift
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  usage >&2
  exit 2
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

if [[ -z "$SOURCE" && -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  if [[ -f "$SCRIPT_DIR/00-AI/scripts/kb.py" ]]; then
    SOURCE="$SCRIPT_DIR"
  fi
fi

if [[ -z "$SOURCE" ]]; then
  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is required for remote install" >&2
    exit 1
  fi
  if ! command -v tar >/dev/null 2>&1; then
    echo "tar is required for remote install" >&2
    exit 1
  fi
  TMP_DIR="$(mktemp -d)"
  ARCHIVE="$TMP_DIR/kit.tar.gz"
  SOURCE="$TMP_DIR/source"
  mkdir -p "$SOURCE"
  echo "downloading ${ARCHIVE_URL}"
  curl -fsSL "$ARCHIVE_URL" -o "$ARCHIVE"
  tar -xzf "$ARCHIVE" -C "$SOURCE" --strip-components=1
fi

if [[ ! -f "$SOURCE/00-AI/scripts/kb.py" ]]; then
  echo "invalid kit source: $SOURCE" >&2
  exit 1
fi

COMMAND="install-core"
if [[ "$UPDATE" -eq 1 ]]; then
  COMMAND="upgrade-core"
fi

ARGS=()
ARGS+=(--mode "$MODE")
ARGS+=(--language "$LANGUAGE")
if [[ "$DRY_RUN" -eq 1 ]]; then
  ARGS+=(--dry-run)
fi
if [[ "$OVERWRITE" -eq 1 ]]; then
  ARGS+=(--overwrite)
fi
if [[ "$ALLOW_PROTECTED_ADAPTER_WRITE" -eq 1 ]]; then
  ARGS+=(--allow-protected-adapter-write)
fi

python3 "$SOURCE/00-AI/scripts/kb.py" "$COMMAND" "$TARGET" "${ARGS[@]}"

if [[ "$DRY_RUN" -eq 0 ]]; then
  cat <<NEXT

Next:
  python3 "$TARGET/00-AI/scripts/kb.py" health-check --vault "$TARGET" --mode "$MODE"

Then send your AI agent:
  You are the knowledge base maintenance agent. Read 00-AI/START-HERE.md in this vault and follow its startup workflow.
NEXT
fi
