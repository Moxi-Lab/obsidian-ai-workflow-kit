# Scripts

These scripts are optional. The vault works without them.

## One-line Install

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone "/path/to/your-vault"
```

The remote installer downloads the current repository archive and delegates to `install-core`.

Modes:

- `full` is the default and installs the complete workflow kit.
- `barebone` installs the smallest usable layer: startup entry, governance, project registry, project bridge template, and `scripts/kb.py`.

## Health Check

```bash
python3 scripts/kb.py health-check
python3 scripts/kb.py health-check --mode barebone
```

Checks:

- Core files and directories exist.
- Legacy private-vault concepts are not present.
- Markdown relative links point to existing files.
- The English README does not contain visible Chinese text.

Use `--mode barebone` when checking a minimal install.

## Install Core

```bash
python3 scripts/kb.py install-core "/path/to/your-vault" --dry-run
python3 scripts/kb.py install-core "/path/to/your-vault"
python3 scripts/kb.py install-core "/path/to/your-vault" --mode barebone --dry-run
python3 scripts/kb.py install-core "/path/to/your-vault" --mode barebone
bash install.sh --dry-run "/path/to/your-vault"
bash install.sh "/path/to/your-vault"
bash install.sh --mode barebone --dry-run "/path/to/your-vault"
bash install.sh --mode barebone "/path/to/your-vault"
```

Copies the core kit into an existing Obsidian vault.

Default behavior:

- Creates missing files and directories.
- Skips existing files.
- Does not overwrite unless `--overwrite` is passed.
- Refuses to install into this kit repository or into a child directory of it.

## New Project

```bash
python3 scripts/kb.py new-project my-project --name "My Project" --root "/path/to/project"
```

Creates:

- `10-Projects/my-project/README.md`
- `10-Projects/my-project/CODEX-BRIDGE-my-project.md`
- `10-Projects/my-project/current-state.md`
- `10-Projects/my-project/decisions.md`

## Intake Source

```bash
python3 scripts/kb.py intake-source "/path/to/source.md" --title "Source Title" --project my-project
```

Creates a source analysis card under `40-ExternalSources/01-samples/`.

Use this when a local file or URL should enter the knowledge pipeline before AI decides whether to promote it into a project update, shared asset, or recall map entry. For folders, use `intake-folder`.

## Intake Folder

```bash
python3 scripts/kb.py intake-folder "/path/to/materials" --title "Materials Intake" --project my-project
```

Creates a folder inventory card under `40-ExternalSources/02-folder-intakes/`.

Default behavior:

- Does not move or edit original files.
- Skips hidden files and common tool folders.
- Lists at most 200 files unless `--max-files` is passed.
- Supports `--extensions md,pdf,txt` for a narrower inventory.

## Audit Vault

```bash
python3 scripts/kb.py audit-vault
python3 scripts/kb.py audit-vault --write-report
```

Checks core entry points, stale concepts, Markdown links, Inbox files, and project directories without bridge cards. `--write-report` writes a report under `20-SharedAssets/05-audit-reports/`.
