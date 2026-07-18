---
type: project-bridge
status: active
project: Launch Notes
local_root: "<your-local-project-path>"
kb_project: "examples/filled-example/README.md"
startup_files:
  - "00-AI/START-HERE.md"
  - "examples/filled-example/current-state.md"
  - "examples/filled-example/decisions.md"
updated: 2026-06-01
---

# Project Bridge | Launch Notes

## One-line Purpose

Launch Notes is a recurring writing project for turning product updates into clear release notes and short launch articles.

## Startup Files

1. `00-AI/START-HERE.md`
2. This bridge card
3. `current-state.md`
4. `decisions.md`

## Current State

- 2026-06-01: The project has one upcoming article about a new onboarding flow.
- Draft outline is ready.
- Source notes are incomplete; the next AI session should ask for missing product facts before writing final copy.
- The owner prefers concise notes with concrete examples and no marketing-heavy language.

## Recent Decisions

- Use one canonical article per launch instead of separate long and short versions.
- Keep release notes under 600 words unless the user asks for a deep dive.
- Do not copy customer quotes unless the source link and permission status are recorded.

## Next Startup

- Read `current-state.md`.
- Check `decisions.md`.
- Ask only for missing product facts.
- Write the next result back to `current-state.md` or create an agent handoff in `01-Inbox/agent-handoffs/`.

## Write-back Rules

| Content | Write Back To |
|---|---|
| Article status | `current-state.md` |
| Stable editorial decisions | `decisions.md` |
| Temporary handoff | `01-Inbox/agent-handoffs/` |
| Reusable writing lesson | `20-SharedAssets/01-user-assets/` |

## Reusable Lessons To Recall

| Situation | Read | Use |
|---|---|---|
| Repeated editorial preference appears | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md` | Turn it into a reusable lesson instead of keeping it in chat |
| External source needs analysis | `40-ExternalSources/README.md` | Summarize the source without copying the full article |
