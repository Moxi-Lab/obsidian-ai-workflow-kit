---
type: base-index
status: active
---

# Obsidian Bases

These dependency-free views are installed only in `full` mode. They use Obsidian's built-in Bases core plugin and do not require Dataview or a community plugin.

- `project-overview.base`: authoritative project entry pages marked with `project_entry: true`.
- `task-overview.base`: queued, active, blocked, completed, and archived local tasks.
- `source-overview.base`: captured external source cards and folder intake manifests.

Markdown pages remain the source of truth. A Base is a view over frontmatter, so every field used by a Base is also guarded by `health-check`.
