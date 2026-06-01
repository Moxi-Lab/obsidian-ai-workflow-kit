# Obsidian AI Memory Kit

[Chinese](README.zh-CN.md) | English

Turn local materials into an AI-maintained Obsidian knowledge base.

Most people already have useful knowledge scattered across local folders, notes, web clips, project documents, and chat history. The problem is not storage. The problem is that AI does not know how to sort it, govern it, recall it, or keep it healthy over time.

Obsidian AI Memory Kit gives your AI agent a working system for organizing your local materials into a clear Obsidian vault with governance rules, recall maps, project memory, source triage, and maintenance loops.

It helps you:

- Sort local files, web clips, notes, and chat conclusions into the right knowledge types.
- Give AI rules for what it may write, where it should write, and what must be verified first.
- Make project state, decisions, source summaries, and reusable lessons easy to recall.
- Keep the vault maintainable with health checks, review gates, and write-back rules.
- Use everything locally with your own private Obsidian vault.

## Quick Start

1. Clone or download this repository.
2. In Obsidian, choose **Open folder as vault** and select the repository folder. No community plugins are required. Obsidian will create its local `.obsidian/` config when you open the folder.
3. Open `START-HERE.md`.
4. Send this instruction to your AI agent:

```text
You are the knowledge base maintenance agent. Read START-HERE.md in the current vault and follow its startup workflow.
```

If your agent is not running from the vault root, include the vault path:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read START-HERE.md in that directory, then follow its startup workflow.
```

You can send it to tools that can read local files, such as Claude Code, Cursor, Codex CLI, or a ChatGPT session where you upload or expose the vault files. If the tool cannot read your local folder directly, use the path-based instruction above.

To organize local materials, give the AI a folder path or a short file list after it reads `START-HERE.md`. It should use the knowledge pipeline instead of scanning everything blindly.

## Why This Exists

Most notes are readable by humans, but not structured enough for AI agents to organize, govern, recall, and maintain reliably.

This kit adds a lightweight operating layer on top of Obsidian:

| Problem | This kit provides |
|---|---|
| AI does not know how to start | `START-HERE.md` as the single entry point |
| Local materials are mixed together | `02-Knowledge-Pipeline/` for intake, classification, extraction, and promotion |
| AI writes too freely | `00-Agent-Governance/` for review gates and write-back rules |
| Useful knowledge is hard to recall | `03-Recall-System/` for task-to-context maps and recall fields |
| Project context is scattered | Project bridge cards in `10-Projects/` |
| External sources get copied blindly | Analysis cards in `40-ExternalSources/` |

## Scope

The kit focuses on four jobs:

- Knowledge pipeline: turn local materials into structured notes.
- Agent governance: control what AI reads, writes, verifies, and avoids.
- Recall system: help AI find the right context for each task.
- Maintenance loop: keep the vault healthy over time.

This is not a RAG stack, a cloud service, or a task manager. It is a local-first operating method for Obsidian plus AI.

## Repository Layout

```text
.
├── START-HERE.md
├── index.md
├── AGENTS.md
├── 00-Agent-Governance/
├── 01-Inbox/
├── 02-Knowledge-Pipeline/
├── 03-Recall-System/
├── 10-Projects/
├── 20-SharedAssets/
├── 40-ExternalSources/
├── 90-Templates/
├── scripts/
└── examples/
```

| Path | Purpose |
|---|---|
| [`START-HERE.md`](START-HERE.md) | The first file an AI agent should read |
| [`index.md`](index.md) | Human-facing vault homepage |
| [`AGENTS.md`](AGENTS.md) | Rules for Codex, Claude Code, and other coding agents |
| [`00-Agent-Governance/`](00-Agent-Governance/) | Startup contract, review gates, write-back rules, maintenance loop |
| [`01-Inbox/`](01-Inbox/) | Temporary handoffs, dispatch cards, and web clips |
| [`02-Knowledge-Pipeline/`](02-Knowledge-Pipeline/) | How AI turns local materials into structured knowledge |
| [`03-Recall-System/`](03-Recall-System/) | Task-to-context maps and recall fields |
| [`10-Projects/`](10-Projects/) | Project workspaces and bridge cards |
| [`20-SharedAssets/`](20-SharedAssets/) | Reusable methods, SOPs, and workflows |
| [`40-ExternalSources/`](40-ExternalSources/) | Source analysis cards, not copied third-party articles |
| [`90-Templates/`](90-Templates/) | Standard templates |
| [`scripts/`](scripts/) | Small helper scripts for project cards and health checks |
| [`examples/`](examples/) | End-to-end handoff demo |

## Core Ideas

### 1. One Entry Point

`START-HERE.md` tells the agent what kind of task it is handling, which files to read first, and where results should be written.

### 2. Knowledge Pipeline

`02-Knowledge-Pipeline/` tells AI how to intake local materials, classify them, extract value, connect them, promote reusable knowledge, and maintain the result.

### 3. Agent Governance

`00-Agent-Governance/` tells AI what it may write, what it must verify, and when it should stop instead of guessing.

### 4. Recall System

`03-Recall-System/` maps tasks to the files AI should read first.

### 5. Project Bridge Cards

Each important project gets a bridge card with the project path, current state, recent decisions, next action, and write-back rules.

Start with:

```text
10-Projects/01-example-project/CODEX-BRIDGE-example.md
```

### 6. Inbox Is Temporary

`01-Inbox/` is for incoming handoffs, task cards, and web clips. It is not a permanent storage area.

### 7. Lessons Become Assets

Repeated lessons should move into `20-SharedAssets/` with a clear trigger, action, and verification method.

### 8. Local-first by Default

This kit is designed to be copied into your own local Obsidian vault. Your real project states, personal notes, handoff history, and private source material stay on your machine.

## Example Workflow

```text
User instruction
  -> START-HERE.md
  -> task-to-context map
  -> governance rules
  -> knowledge pipeline or project bridge card
  -> structured write-back
  -> reusable lesson enters Recall System
```

Try the demo:

```text
examples/ai-handoff-demo/README.md
```

For a more realistic filled example, see:

```text
examples/filled-example/
```

For a source-to-knowledge example, see:

```text
examples/source-to-knowledge/
```

Daily use should stay small: after the first setup, most agent sessions only need `START-HERE.md`, one project bridge card, and that project's `current-state.md` / `decisions.md`.

If you already have an Obsidian vault, start with [MIGRATION.md](MIGRATION.md). Do not rebuild your vault; add one project bridge card first.

## Optional Scripts

The vault works without scripts. If you want a faster setup loop:

```bash
python3 scripts/kb.py health-check
python3 scripts/kb.py new-project my-project --name "My Project" --root "/path/to/project"
python3 scripts/kb.py intake-source "/path/to/source.md" --title "Source Title" --project my-project
```

`health-check` verifies the core files, common stale concepts, and Markdown links. `new-project` creates a minimal project workspace and bridge card under `10-Projects/`. `intake-source` creates a source analysis card that AI can refine.

## Included Templates

| Template | Use |
|---|---|
| [Project Bridge Card](90-Templates/TPL-Codex%E9%A1%B9%E7%9B%AE%E6%A1%A5%E6%8E%A5%E5%8D%A1.md) | Project handoff and continuation |
| [Agent Handoff Card](90-Templates/TPL-Agent%E4%BA%A4%E6%8E%A5%E5%8D%A1.md) | End-of-session handoff |
| [Source Analysis Card](90-Templates/TPL-%E8%B5%84%E6%96%99%E5%88%86%E6%9E%90%E5%8D%A1.md) | External source analysis |
| [Task State Card](90-Templates/TPL-%E4%BB%BB%E5%8A%A1%E7%8A%B6%E6%80%81%E5%8D%A1.md) | Task state tracking |
| [Acceptance Record](90-Templates/TPL-%E9%AA%8C%E6%94%B6%E8%AE%B0%E5%BD%95.md) | Acceptance record |
| [Question Knowledge / Experience Asset Card](90-Templates/TPL-%E9%97%AE%E9%A2%98%E7%9F%A5%E8%AF%86%E5%8D%A1-%E7%BB%8F%E9%AA%8C%E8%B5%84%E4%BA%A7%E5%8D%A1.md) | Reusable question and experience asset |
| [Web Clip Minimal Template](90-Templates/TPL-WebClip-%E6%9C%80%E7%AE%80%E6%A8%A1%E6%9D%BF.md) | Raw Web Clipper capture |

## Not Included

This repository intentionally excludes:

- Personal profiles, preferences, and real project states.
- Full third-party articles, X posts, web clips, or long translations.
- Trading records, account information, or strategy runtime state.
- Agent run logs and private handoff history.
- Local paths, sync scripts, API keys, tokens, cookies, private keys, passwords, and verification codes.

## License

- Original written content: CC BY 4.0.
- Code, scripts, and executable snippets: MIT.
- Third-party content is not covered by this repository license.

## Version

Current version: `0.4.0`. See [CHANGELOG.md](CHANGELOG.md).
