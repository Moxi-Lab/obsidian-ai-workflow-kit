# Obsidian AI Memory Kit

[Chinese](README.zh-CN.md) | English

Stop re-explaining your projects to AI.

If you use Obsidian for real work, your vault already contains what an AI agent needs: project context, decisions, references, lessons, and unfinished threads. The problem is that most of it is not arranged for handoff. Every new AI session still starts cold.

Obsidian AI Memory Kit turns that private knowledge into a reusable working memory layer, so an AI agent can behave less like a first-time assistant and more like someone who has been following the project.

It helps you:

- Spend less time reloading context for every AI session.
- Keep project decisions, current state, and next actions in places AI can reliably find.
- Turn repeated fixes and lessons into reusable assets instead of losing them in chat history.
- Use it locally with your own private Obsidian vault.
- Make Obsidian feel like a long-term workspace for human + AI collaboration, not just a note archive.

## Quick Start

1. Copy this repository as a new Obsidian vault.
2. Open `START-HERE.md`.
3. Send this instruction to your AI agent:

```text
You are the knowledge base maintenance agent. Read START-HERE.md in the current vault and follow its startup workflow.
```

If your agent is not running from the vault root, include the vault path:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read START-HERE.md in that directory, then follow its startup workflow.
```

With the demo project, the agent should be able to find the project card, read the current state, complete a task, and write the result back to the right place.

## Why This Exists

Most notes are readable by humans, but not structured enough for AI agents to resume project work reliably.

This kit adds a lightweight operating layer on top of Obsidian:

| Problem | This kit provides |
|---|---|
| AI does not know where to start | `START-HERE.md` as the single entry point |
| Project context is scattered | Project bridge cards in `10-Projects/` |
| Useful lessons stay in chat history | Reusable assets in `20-SharedAssets/` |
| Temporary notes become clutter | Inbox flow in `01-Inbox/` |
| External sources get copied blindly | Analysis cards in `40-ExternalSources/` |
| Every agent works differently | Shared rules in `AGENTS.md` and `00-Agent-OS-Lite/` |

## Scope

The kit focuses on three jobs:

- Project memory: keep current state, decisions, and next actions easy for AI to find.
- Reusable lessons: turn repeated fixes into assets instead of chat history.
- Source triage: summarize external material without copying full third-party content.

Maintenance rules only exist to keep those three jobs usable. This is not a full personal knowledge management system, a RAG stack, or a task manager.

## Repository Layout

```text
.
├── START-HERE.md
├── index.md
├── AGENTS.md
├── 00-Agent-OS-Lite/
├── 01-Inbox/
├── 02-MOCs/
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
| [`00-Agent-OS-Lite/`](00-Agent-OS-Lite/) | Minimal startup rules, registry, and health-check sample |
| [`01-Inbox/`](01-Inbox/) | Temporary handoffs, dispatch cards, and web clips |
| [`02-MOCs/`](02-MOCs/) | Optional human-readable maps of content |
| [`10-Projects/`](10-Projects/) | Project workspaces and bridge cards |
| [`20-SharedAssets/`](20-SharedAssets/) | Reusable methods, SOPs, and workflows |
| [`40-ExternalSources/`](40-ExternalSources/) | Source analysis cards, not copied third-party articles |
| [`90-Templates/`](90-Templates/) | Standard templates |
| [`scripts/`](scripts/) | Small helper scripts for project cards and health checks |
| [`examples/`](examples/) | End-to-end handoff demo |

## Core Ideas

### 1. One Entry Point

`START-HERE.md` tells the agent what kind of task it is handling, which files to read first, and where results should be written.

### 2. Project Bridge Cards

Each important project gets a bridge card with the project path, current state, recent decisions, next action, and write-back rules.

Start with:

```text
10-Projects/01-example-project/CODEX-BRIDGE-example.md
```

### 3. Inbox Is Temporary

`01-Inbox/` is for incoming handoffs, task cards, and web clips. It is not a permanent storage area.

### 4. Lessons Become Assets

Repeated lessons should move into `20-SharedAssets/` with a clear trigger, action, and verification method.

### 5. Local-first by Default

This kit is designed to be copied into your own local Obsidian vault. Your real project states, personal notes, handoff history, and private source material stay on your machine.

## Example Workflow

```text
User instruction
  -> START-HERE.md
  -> project bridge card
  -> current state / decisions
  -> task execution
  -> write back to project or Inbox
  -> reusable lesson goes to SharedAssets
```

Try the demo:

```text
examples/ai-handoff-demo/README.md
```

## Optional Scripts

The vault works without scripts. If you want a faster setup loop:

```bash
python3 scripts/kb.py health-check
python3 scripts/kb.py new-project my-project --name "My Project" --root "/path/to/project"
```

`health-check` verifies the core files, common stale concepts, and Markdown links. `new-project` creates a minimal project workspace and bridge card under `10-Projects/`.

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
