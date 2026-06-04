---
type: entry
status: active
aliases: ["Start Here"]
language: en
---

# START HERE

Language: English

> Read this file first in every new AI session. It tells the agent what to read, where to write, and what not to do.

## Startup Prompt

```text
You are the knowledge base maintenance agent. Read 00-AI/START-HERE.md in the current vault and follow its startup workflow.
```

If the agent did not start from the vault root, include the vault path:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read 00-AI/START-HERE.md in that directory, then follow its startup workflow.
```

## Required First Reply

After reading this file, the agent should reply in this shape before scanning the vault:

```text
Read: 00-AI/START-HERE.md
Task type: <local material intake / project handoff / external source processing / lesson capture / vault maintenance / handoff writing / needs clarification>
Next file to read: <specific file>
Write-back target: <specific folder or file>
Will not do: <explicit out-of-scope work for this session>
```

## Startup Steps

### 1. Identify The Task Type

| Task type | Read first |
|---|---|
| Local material intake | `00-AI/pipeline/README.md`, `00-AI/pipeline/local-material-intake.md` |
| Project handoff | `10-Projects/<project>/BRIDGE-*.md` |
| External source processing | `40-ExternalSources/README.md`, `00-AI/templates/TPL-source-analysis-card.md` |
| Lesson capture | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`, `00-AI/templates/TPL-question-knowledge-experience-asset-card.md` |
| Incident review | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`, `00-AI/templates/TPL-incident-experience-card.md` |
| Vault maintenance | `00-AI/governance/maintenance-loop.md`, `20-SharedAssets/02-modules/vault-health-checklist-v1.md` |
| Handoff writing | `00-AI/templates/TPL-agent-handoff-card.md` |

### 2. Load Only Necessary Context

- Read `index.md` and this file first.
- Read `00-AI/governance/README.md` only when governance rules are needed.
- Read `00-AI/recall/task-to-context-map.md` only when recall rules are needed.
- For project work, read only the relevant project bridge card.
- Do not scan the whole vault by default.

### 3. Write Back To The Right Place

| Content | Write to |
|---|---|
| Temporary handoff | `01-Inbox/agent-handoffs/` |
| Dispatch card | `01-Inbox/dispatch-cards/` |
| External source analysis | `40-ExternalSources/01-samples/` or a relevant topic folder |
| Project state | The relevant project bridge card |
| Reusable lesson | `20-SharedAssets/02-modules/` |
| Incident lesson | Copy `00-AI/templates/TPL-incident-experience-card.md` into the relevant project or shared asset location |
| Recall rule | `00-AI/recall/` |
| Template | `00-AI/templates/` |

## Do Not

- Do not save secrets, tokens, cookies, verification codes, private keys, or account credentials.
- Do not treat raw chat logs as long-term memory.
- Do not copy full third-party articles into the vault.
- Do not use Inbox folders as permanent storage.
- Do not reorganize the vault without a clear task.

## Before Ending

- State what changed.
- State why it changed.
- State what was verified.
- State whether memory was updated; if not, say no memory was written.
