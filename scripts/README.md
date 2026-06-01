# Scripts

These scripts are optional. The vault works without them.

## Health Check

```bash
python3 scripts/kb.py health-check
```

Checks:

- Core files and directories exist.
- Legacy private-vault concepts are not present.
- Markdown relative links point to existing files.
- The English README does not contain visible Chinese text.

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

Use this when a local file, folder, or URL should enter the knowledge pipeline before AI decides whether to promote it into a project update, shared asset, or recall map entry.
