# Obsidian AI Workflow Kit

[Chinese](README.zh-CN.md) | English

[![CI](https://github.com/Moxi-Lab/obsidian-ai-workflow-kit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Moxi-Lab/obsidian-ai-workflow-kit/actions/workflows/ci.yml)

Make your local Obsidian vault readable, writable, and maintainable by AI agents.

You open a new Claude Code, Cursor, Codex, or ChatGPT session. It asks what this project is, where the important context lives, and what changed last time. Again.

This kit fixes that handoff problem with a local-first Obsidian structure: one startup entry, project bridge cards, write-back rules, source triage, recall maps, and maintenance checks.

It is not an app, plugin, cloud memory service, or RAG stack. It is a file-system-level workflow that humans can edit and any AI agent with file access can follow.

## Start Fast

### Existing Vault

Recommended first step: install the minimal layer into your own vault.

Preview:

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone --dry-run "/path/to/your-vault"
```

Install:

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone "/path/to/your-vault"
```

Check:

```bash
python3 "/path/to/your-vault/scripts/kb.py" health-check --vault "/path/to/your-vault" --mode barebone
```

Then send this to your AI agent:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read START-HERE.md in that directory, then follow its startup workflow.
```

Use full mode when you want the complete starter vault, including pipeline, recall system, docs, examples, and templates:

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- "/path/to/your-vault"
```

The installer skips existing files by default. Pass `--overwrite` only when you intentionally want to replace files.

### Demo Vault

1. Clone or download this repository.
2. In Obsidian, choose **Open folder as vault** and select the repository folder.
3. Open `START-HERE.md`.
4. Send the AI startup instruction above.

No Obsidian community plugins are required.

## What You Get

| Need | Included layer |
|---|---|
| AI needs a clear start point | `START-HERE.md` |
| Project context is scattered | project bridge cards in `10-Projects/` |
| AI writes too freely | governance rules in `00-Agent-Governance/` |
| Local materials need sorting | knowledge pipeline in `02-Knowledge-Pipeline/` |
| Useful lessons are hard to recall | task maps and recall fields in `03-Recall-System/` |
| The vault slowly gets messy | health checks and maintenance rules |

## How It Works

![Obsidian AI Workflow Kit architecture](docs/images/architecture-flow.png)

Daily use stays small:

```text
User task
  -> START-HERE.md
  -> relevant project bridge card or task map
  -> required context only
  -> structured write-back
  -> reusable lessons promoted for future recall
```

The agent should not scan your whole vault by default. It should read the startup entry, open the mapped context, do the task, and write results back to the right place.

## Install Modes

| Mode | Best for | What it installs |
|---|---|---|
| `barebone` | First step inside an existing vault | startup entry, governance, project registry, project bridge template, `scripts/kb.py` |
| `full` | New starter vault or complete trial | all workflow folders, examples, docs, templates, scripts |

Security-sensitive users can skip the remote `curl` form and run the installer from a local clone:

```bash
bash install.sh --mode barebone --dry-run "/path/to/your-vault"
bash install.sh --mode barebone "/path/to/your-vault"
```

## Is This For You?

Good fit:

- You already use Obsidian for project notes, sources, or decisions.
- You use AI agents often enough that context handoff is painful.
- You want local-first memory that remains human editable.
- You are willing to keep project state and handoffs current.

Not a good fit:

- You want a graphical Obsidian plugin.
- You want a cloud memory service or managed RAG backend.
- You want AI to scan your whole computer automatically.
- You want automatic bulk rewriting of an existing vault.

## Learn More

- [10-Minute First Run](docs/10-minute-first-run.md)
- [Before / After Case](docs/before-after-case.md)
- [Migration Guide](MIGRATION.md)
- [Concepts](docs/concepts.md)
- [Templates](docs/templates.md)
- [Scripts](scripts/README.md)
- [Release Checklist](RELEASE_CHECKLIST.md)

## Repository Layout

```text
START-HERE.md              AI startup entry
00-Agent-Governance/       write-back, review, and maintenance rules
02-Knowledge-Pipeline/     local material intake and promotion
03-Recall-System/          task-to-context maps and recall fields
10-Projects/               project workspaces and bridge cards
20-SharedAssets/           reusable methods and lessons
40-ExternalSources/        source analysis cards
90-Templates/              reusable note templates
docs/                      guides, diagrams, and walkthroughs
scripts/                   optional helper scripts
examples/                  demo project and source workflows
```

Some source filenames are not English because they come from the original working method. The English entry points are `README.md`, `START-HERE.md`, `AGENTS.md`, `index.md`, and the docs linked above.

## Maturity

This is a `0.x` beta starter kit. It is ready for controlled trials, small vaults, and feedback. It does not promise compatibility with every existing Obsidian vault layout.

This is a workflow kit, not an automation platform. If project state, decisions, handoffs, and reusable lessons are not maintained, the vault will slowly become ordinary folders again.

## License

- Code, scripts, and executable snippets: [MIT](LICENSE).
- Original written content, templates, examples, and documentation: [CC BY 4.0](CONTENT-LICENSE.md).
- Third-party content is not covered by this repository license.

## Version

Current version: `0.5.7`. See [CHANGELOG.md](CHANGELOG.md).
