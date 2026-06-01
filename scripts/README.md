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

## Update Existing Install

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone --dry-run "/path/to/your-vault"
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --update --mode barebone "/path/to/your-vault"
```

`--update` upgrades managed kit files from the latest GitHub version. It uses `.obsidian-ai-workflow-kit/manifest.json` to tell whether a file is still the original kit file or has been changed by the user.

Default behavior:

- Creates new kit files that were added after your install.
- Updates kit files that are still unmodified.
- Skips files that were edited by the user.
- Skips existing files that were never recorded in the manifest.
- Refuses to write into vaults protected by `.obsidian-ai-workflow-kit/adoption-policy.json`.

Use `--conflict-copy` with `upgrade-core` when you want new versions written beside conflicted files for manual comparison:

```bash
python3 scripts/kb.py upgrade-core "/path/to/your-vault" --mode barebone --conflict-copy
```

## Local Adapter Protection

A vault can consume this kit as an architecture reference without becoming a managed kit install. Add this file to the vault:

```json
{
  "mode": "local-adapter",
  "allow_public_kit_writes": false
}
```

Path:

```text
.obsidian-ai-workflow-kit/adoption-policy.json
```

When this policy exists, `install-core` and `upgrade-core` refuse to write kit files into the vault. `--dry-run` still works for review. Only use `--allow-protected-adapter-write` after an explicit manual decision.

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

## Stale Check

```bash
python3 scripts/kb.py stale-check --vault "/path/to/your-vault"
python3 scripts/kb.py stale-check --vault "/path/to/your-vault" --max-age-days 7 --inbox-threshold 10 --fail-on-findings
```

Reports project bridge cards with old or missing `updated` dates and Inbox folders that exceed the file threshold. Use `--fail-on-findings` for hooks or CI jobs that should stop when review items exist.

## Migrate Legacy Codex Names

```bash
python3 scripts/kb.py migrate-codex-names --vault "/path/to/your-vault" --dry-run
python3 scripts/kb.py migrate-codex-names --vault "/path/to/your-vault"
```

Renames older Codex-specific files to the current agent-neutral names and updates Markdown references.

Examples:

- `CODEX-BRIDGE-my-project.md` -> `BRIDGE-my-project.md`
- `TPL-Codex项目桥接卡.md` -> `TPL-project-bridge-card.md`
- `Codex项目经验资产化机制-v1.md` -> `project-lesson-promotion-v1.md`

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
- Records managed kit files in `.obsidian-ai-workflow-kit/manifest.json` so future updates can be safer.
- Refuses to install into this kit repository or into a child directory of it.

## Upgrade Core

```bash
python3 scripts/kb.py upgrade-core "/path/to/your-vault" --mode barebone --dry-run
python3 scripts/kb.py upgrade-core "/path/to/your-vault" --mode barebone
```

Use this when a vault already has the kit and you want to follow newer GitHub versions without replacing user-owned notes. It only updates files that are managed by the kit and still match the last installed checksum.

## New Project

```bash
python3 scripts/kb.py new-project my-project --name "My Project" --root "/path/to/project"
```

Creates:

- `10-Projects/my-project/README.md`
- `10-Projects/my-project/BRIDGE-my-project.md`
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
