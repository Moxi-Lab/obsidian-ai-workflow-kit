# Concepts

This page holds the detail that used to make the README too long.

## What Problem It Solves

AI agents are getting better at doing work, but they still lose the thread when the conversation window changes. Existing memory solutions usually live inside one tool, require infrastructure, or produce a search index that humans cannot comfortably maintain.

This repository adds an AI-readable operating convention to Obsidian, a place many people already use as their local knowledge filesystem.

| Approach | What it is | Limitation |
|---|---|---|
| Claude Code memory files | Tool-specific memory | Tied to one tool and one workflow |
| Cursor Rules | Project-level instructions | Mostly code-focused, weak for sources, lessons, and vault maintenance |
| Vector memory systems | Embedded memory storage | Requires infrastructure and is hard to inspect or edit manually |
| Plain Obsidian / Notion notes | Human notes | AI does not know the entry point, priority, or write-back rules |
| RAG plugins | Full-text retrieval | Recall can be noisy, with weak task mapping and priority control |
| This kit | AI-readable Obsidian operating convention | Local files, human editable, tool agnostic, task mapped |

## Core Ideas

### 1. One Entry Point

`00-AI/START-HERE.md` tells the agent what kind of task it is handling, which files to read first, and where results should be written.

### 2. Knowledge Pipeline

`00-AI/pipeline/` tells AI how to intake local materials, classify them, extract value, connect them, promote reusable knowledge, and maintain the result.

### 3. Agent Governance

`00-AI/governance/` tells AI what it may write, what it must verify, and when it should stop instead of guessing.

### 4. Recall System

`00-AI/recall/` maps tasks to the files AI should read first.

### 5. Project Bridge Cards

Each important project gets a bridge card with the project path, current state, recent decisions, next action, and write-back rules.

Start with:

```text
10-Projects/01-example-project/BRIDGE-example.md
```

### 6. Inbox Is Temporary

`01-Inbox/` is for incoming handoffs, task cards, and web clips. It is not a permanent storage area.

The current conversation is the default execution context. Create `01-Inbox/tasks/` cards only when work is queued, crosses sessions, waits on an external condition, or needs explicit coordination. The default flow does not assign CEO/CTO/QA-style job roles.

### 7. Lessons Become Assets

Repeated lessons should move into `20-SharedAssets/` with a clear trigger, action, and verification method.

Failures, wrong assumptions, rework, failed tests, user corrections, and tool incidents should become incident lessons when they can prevent the same mistake later.

### 8. Local-first By Default

This kit is designed to be copied into your own local Obsidian vault. Your real project states, personal notes, handoff history, and private source material stay on your machine.

### 9. Markdown Is Truth, Bases Are Views

Full mode includes project, task, and source dashboards built with Obsidian's core Bases plugin. `project_entry`, typed `status`, `pillar`, and `captured` are index fields guarded by the read-only health check. A Base never replaces the authoritative Markdown page.

## Scope

The kit focuses on four jobs:

- Knowledge pipeline: turn local materials into structured notes.
- Agent governance: control what AI reads, writes, verifies, and avoids.
- Recall system: help AI find the right context for each task.
- Maintenance loop: keep the vault healthy over time.

This is not a RAG stack, a cloud service, or a hosted task manager. It is a local-first operating method for Obsidian plus AI.

## Example Workflow

```text
User instruction
  -> 00-AI/START-HERE.md
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

Daily use should stay small: after the first setup, most agent sessions only need `00-AI/START-HERE.md`, one project bridge card, and that project's `current-state.md` / `decisions.md`.

If you already have an Obsidian vault, start with [Migration Guide](migration.md). Do not rebuild your vault; add one project bridge card first.

## Repository Layout

| Path | Purpose |
|---|---|
| [`00-AI/START-HERE.md`](../00-AI/START-HERE.md) | The first file an AI agent should read |
| [`index.md`](../index.md) | Human-facing vault homepage |
| [`00-AI/AGENTS.md`](../00-AI/AGENTS.md) | Rules for AI agents such as Claude Code, Cursor, and Codex |
| [`00-AI/governance/`](../00-AI/governance/) | Startup contract, review gates, write-back rules, maintenance loop |
| [`01-Inbox/`](../01-Inbox/) | Temporary handoffs, queued/cross-session task cards, and web clips |
| [`00-AI/pipeline/`](../00-AI/pipeline/) | How AI turns local materials into structured knowledge |
| [`00-AI/recall/`](../00-AI/recall/) | Task-to-context maps and recall fields |
| [`00-AI/bases/`](../00-AI/bases/) | Optional project, task, and source views installed in full mode |
| [`10-Projects/`](../10-Projects/) | Project workspaces and bridge cards |
| [`20-SharedAssets/`](../20-SharedAssets/) | Reusable methods, SOPs, and workflows |
| [`40-ExternalSources/`](../40-ExternalSources/) | Source analysis cards, not copied third-party articles |
| [`00-AI/templates/`](../00-AI/templates/) | Standard templates |
| [`docs/`](./) | First-run guides, diagrams, and user-facing walkthroughs |
| [`00-AI/scripts/`](../00-AI/scripts/) | Small helper scripts for project cards and health checks |
| [`examples/`](../examples/) | End-to-end handoff demo |

Core filenames are English for agent readability. Some page titles and template body text still include Chinese because they preserve the original working method; this does not affect how the workflow runs.
