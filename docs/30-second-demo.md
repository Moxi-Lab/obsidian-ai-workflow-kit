# 30-Second Demo

Use this when you want to see the kit work before installing it into your own vault.

## Steps

1. Download or clone this repository.
2. Open Obsidian, choose **Open folder as vault**, and select this repository folder. A vault is just a local folder of Markdown files.
3. Send this to an AI agent that can read local files:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <path-to-this-repository>. First read 00-AI/START-HERE.md, then use the read-only demo in examples/filled-example. Tell me the current project state, the latest decision, and the next action. Do not edit files, create a task card, or assign a job role.
```

## Expected Result

The agent should read:

- `00-AI/START-HERE.md`
- `index.md`
- `examples/filled-example/BRIDGE-launch-notes.md`
- `examples/filled-example/current-state.md`
- `examples/filled-example/decisions.md`

It should answer with the demo project's current state, latest decision, next action, and where real work would be written back.
