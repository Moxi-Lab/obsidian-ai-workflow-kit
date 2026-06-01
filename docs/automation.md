# Automation Starter

This kit starts as plain Markdown because the rules should stay inspectable. Automation should reduce forgetting, not hide important changes.

Start with reminders and checks:

1. Run `stale-check` before or after AI sessions.
2. Use a Claude Code Stop hook to remind the agent before a session ends.
3. Let the agent write handoffs and project updates by following `START-HERE.md`.

Do not start with silent automatic rewrites. A local knowledge base is safer when humans can see what changed.

## Stale Check

```bash
python3 scripts/kb.py stale-check --vault "/path/to/your-vault"
```

It reports:

- project bridge cards whose `updated` date is older than the threshold;
- bridge cards missing an `updated` date;
- Inbox folders with too many files waiting to be processed.

Use stricter settings when you want the command to fail in hooks or CI:

```bash
python3 scripts/kb.py stale-check \
  --vault "/path/to/your-vault" \
  --max-age-days 7 \
  --inbox-threshold 10 \
  --fail-on-findings
```

## Claude Code Hooks

Claude Code supports project hooks through `.claude/settings.json`. The example in this repository uses a Stop hook: when the session is about to end, it runs `stale-check` and asks the agent to review stale items before stopping.

See the example:

```text
examples/claude-code-hooks/
```

Basic setup:

1. In your vault, create `.claude/hooks/`.
2. Copy `examples/claude-code-hooks/stop-session-check.py` to `.claude/hooks/stop-session-check.py`.
3. Merge `examples/claude-code-hooks/settings.example.json` into `.claude/settings.json`.
4. Start Claude Code from the vault root.

The hook does not edit notes. It only checks whether the session should leave a handoff, update a project bridge card, or clear Inbox items.

Official Claude Code hook docs: <https://docs.anthropic.com/en/docs/claude-code/hooks>

## Suggested Automation Ladder

| Level | Automation | Risk |
|---|---|---|
| 1 | Run `stale-check` manually | Lowest |
| 2 | Stop hook reminds the agent to write handoff | Low |
| 3 | Scheduled `stale-check` writes a report | Medium |
| 4 | AI proposes bridge-card updates from handoffs | Medium |
| 5 | AI directly edits bridge cards without review | High |

This public kit currently ships levels 1 and 2. Higher levels should be added only after the user can inspect and approve changes.
