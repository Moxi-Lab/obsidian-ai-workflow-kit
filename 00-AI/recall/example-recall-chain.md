---
type: recall-example
status: active
updated: 2026-06-02
---

# Example Recall Chain

This example shows how a reusable lesson becomes something a future AI agent can find without scanning the whole vault.

## Scenario

A user asks:

```text
Help me write launch notes for the new onboarding flow.
```

## Recall Path

1. Read `00-AI/START-HERE.md`.
2. Classify the task as launch writing and project continuation.
3. Read `00-AI/recall/task-to-context-map.md`.
4. Open the real project bridge card selected for the current task.
5. Read only the startup files listed by that bridge card.
6. Check reusable lessons listed in the bridge card.
7. Read the relevant promoted lesson from `20-SharedAssets/01-user-assets/`.

## Why The Lesson Is Recalled

The question card contains:

```yaml
applicable_to:
  - onboarding review
  - launch writing
  - product research synthesis
themes:
  - onboarding
  - knowledge-promotion
canonical: true
```

Because the new task mentions launch notes and onboarding, the AI agent should treat this card as relevant before writing.

## Expected Agent Behavior

The agent should:

- Use the bridge card for project state and write-back location.
- Use `current-state.md` for current progress.
- Use `decisions.md` for stable editorial decisions.
- Use the recalled question card as a checklist for when source material should become reusable knowledge.
- Avoid reading unrelated project folders or scanning the entire vault.

## Write-back After The Task

| Result | Write back to |
|---|---|
| Changed project status | The real project bridge card or its current-state page |
| Stable editorial decision | The real project's decisions page |
| Temporary handoff | `01-Inbox/agent-handoffs/` |
| Reusable lesson | `20-SharedAssets/01-user-assets/` or a question knowledge card |

## Maintenance Note

If the project bridge card is stale, the AI agent should tell the user before doing long work and suggest updating:

- the bridge card `last_verified` field after a real fact check
- the current state section
- the next startup action
