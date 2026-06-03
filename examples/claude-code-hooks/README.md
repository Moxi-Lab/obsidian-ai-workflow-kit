# Claude Code Hooks Example

This example shows a conservative Stop hook for Obsidian AI Workflow Kit.

When Claude Code is about to end a session, the hook runs:

```bash
python3 00-AI/scripts/kb.py stale-check --vault .
```

If stale items exist, the hook asks Claude Code to pause and review whether it should write a handoff, update a project bridge card, or clear Inbox items.

## Files

- `settings.example.json`: example `.claude/settings.json` fragment.
- `stop-session-check.py`: command hook script.

## Install

From your vault root:

```bash
mkdir -p .claude/hooks
cp examples/claude-code-hooks/stop-session-check.py .claude/hooks/stop-session-check.py
```

Then merge `settings.example.json` into `.claude/settings.json`.

The hook is advisory. It does not edit your notes automatically.
