# 10-Minute First Run

This path is for a new user who wants to see value quickly without rebuilding an existing vault.

## 0. Start With A Test Vault

Use an empty folder or a small existing vault. Do not start with your full personal vault.

```bash
mkdir -p ~/obsidian-ai-workflow-test
mkdir -p ~/demo-materials
printf "Example note for folder intake.\n" > ~/demo-materials/example.md
```

## 1. Preview Installation

If this repository is public:

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --dry-run ~/obsidian-ai-workflow-test
```

If you cloned the repository:

```bash
bash install.sh --dry-run ~/obsidian-ai-workflow-test
```

## 2. Install

If this repository is public:

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- ~/obsidian-ai-workflow-test
```

If you cloned the repository:

```bash
bash install.sh ~/obsidian-ai-workflow-test
```

The installer skips existing files by default.

## 3. Verify

```bash
python3 ~/obsidian-ai-workflow-test/00-AI/scripts/kb.py health-check --vault ~/obsidian-ai-workflow-test --mode barebone
```

## 4. Create A Project Bridge

```bash
python3 ~/obsidian-ai-workflow-test/00-AI/scripts/kb.py new-project demo-project \
  --vault ~/obsidian-ai-workflow-test \
  --name "Demo Project" \
  --root ~/demo-project
```

## 5. Create A Folder Intake

Point this at a small folder with a few documents:

```bash
python3 ~/obsidian-ai-workflow-test/00-AI/scripts/kb.py intake-folder ~/demo-materials \
  --vault ~/obsidian-ai-workflow-test \
  --title "Demo Materials" \
  --project demo-project
```

This creates a manifest only. It does not move or edit original files.

## 6. Ask An AI Agent To Start

Send this to any AI tool that can read local files:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: ~/obsidian-ai-workflow-test. First read 00-AI/START-HERE.md in that directory, then follow its startup workflow.
```

Expected first response:

```text
Read 00-AI/START-HERE.md
Task type: <...>
Next files to read: <...>
Write-back target: <...>
Will not do: <...>
```

## 7. Run A Vault Audit

```bash
python3 ~/obsidian-ai-workflow-test/00-AI/scripts/kb.py audit-vault \
  --vault ~/obsidian-ai-workflow-test \
  --write-report
```

The report is written to:

```text
20-SharedAssets/05-audit-reports/
```

## Success Criteria

You should now have:

- One AI startup entry.
- One project bridge card.
- One folder intake manifest.
- One audit report.
- A clear instruction you can give to an AI agent.
