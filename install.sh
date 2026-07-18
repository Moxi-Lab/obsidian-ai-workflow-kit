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
MODE="barebone"
LANGUAGE="en"
TARGET=""
TMP_DIR=""

usage() {
  cat <<'USAGE'
Install Obsidian AI Workflow Kit into an existing Obsidian vault.

Usage:
  bash install.sh [--dry-run] [--overwrite] [--update] [--allow-protected-adapter-write] [--language en|zh-CN] [--branch main] [--source /path/to/repo] <vault-path>

Examples:
  bash install.sh --dry-run "/path/to/your-vault"
  bash install.sh "/path/to/your-vault"
  bash install.sh --language zh-CN "/path/to/your-vault"
  bash install.sh --update --dry-run "/path/to/your-vault"
  bash install.sh --update "/path/to/your-vault"

Remote one-line form:
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --dry-run "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --dry-run "/path/to/your-vault"
  curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update "/path/to/your-vault"

Default behavior:
  - Creates missing files and directories.
  - Skips existing files.
  - Does not overwrite unless --overwrite is passed.
  - In --update mode, only managed and unmodified kit files are updated.
  - Refuses to write into vaults protected by .obsidian-ai-workflow-kit/adoption-policy.json unless --allow-protected-adapter-write is passed.
  - Installs the minimal starter template by default. Use --mode shared-core for an established managed vault.
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
      if [[ "$2" != "full" && "$2" != "barebone" && "$2" != "shared-core" ]]; then
        echo "mode must be full, barebone, or shared-core" >&2
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
  if [[ "$LANGUAGE" == "zh-CN" ]]; then
    HELPER_PATH="90-系统/脚本/kb.py"
    START_PATH="00-入口/开始这里.md"
    AGENT_PROMPT="你是知识库维护 Agent。请读取当前 vault 的 00-入口/开始这里.md，并按里面的开工流程执行。"
  else
    HELPER_PATH="00-AI/scripts/kb.py"
    START_PATH="00-AI/START-HERE.md"
    AGENT_PROMPT="You are the knowledge base maintenance agent. Read 00-AI/START-HERE.md in this vault and follow its startup workflow."
  fi
  cat <<NEXT

Next:
  python3 "$TARGET/$HELPER_PATH" health-check --vault "$TARGET" --mode "$MODE"

Then send your AI agent:
  $AGENT_PROMPT

Startup file:
  $TARGET/$START_PATH
NEXT
fi
