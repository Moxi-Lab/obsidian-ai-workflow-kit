# Migration Guide

Use this kit gradually. Do not rebuild an existing Obsidian vault.

## If You Are Starting Fresh

1. Clone or download this repository.
2. Open the folder in Obsidian with **Open folder as vault**.
3. Read `START-HERE.md`.
4. Create your first real project bridge card:

```bash
python3 scripts/kb.py new-project my-project --name "My Project" --root "/path/to/project"
```

5. Fill only three files first:

- `10-Projects/my-project/CODEX-BRIDGE-my-project.md`
- `10-Projects/my-project/current-state.md`
- `10-Projects/my-project/decisions.md`

## If You Already Have a Vault

1. Copy only these files and folders into your existing vault:

- `START-HERE.md`
- `AGENTS.md`
- `10-Projects/`
- `20-SharedAssets/`
- `40-ExternalSources/`
- `90-Templates/`
- `scripts/`

2. Do not move all existing notes.
3. Pick one active project.
4. Create one bridge card for that project.
5. Link existing notes from the bridge card instead of reorganizing them.

## First Project Bridge Card

A useful first bridge card should answer:

- What project is this?
- Where is the local project folder?
- What is the current state?
- What decisions are stable?
- What should the next AI session read first?
- Where should the result be written back?

## What Not To Migrate

- Full chat history.
- Temporary scratch notes.
- Old web clips without source value.
- Private credentials or account data.
- Every note in your vault.

## Good First Acceptance Check

After migration, give an AI agent this instruction:

```text
You are the knowledge base maintenance agent. Read START-HERE.md in the current vault and follow its startup workflow.
```

The agent should identify one project bridge card, read only the needed project files, and say where it will write results back.
