---
type: projects-readme
status: active
---

# Projects

这里放需要 AI 多次接手的项目。

## 项目登记

- `PROJECTS-REGISTRY.md`：登记需要 AI 多次接手的项目。

每个项目至少包含：

- `README.md`：人类看的项目入口。
- `BRIDGE-*.md`：AI 接手用的桥接卡。
- `current-state.md`：当前状态。
- `decisions.md`：稳定决策。

每个长期项目只能有一个权威入口页设置 `project_entry: true`。默认由 `BRIDGE-*.md` 承担，并同时填写 `project / pillar / status / updated`。Full 模式的 `00-AI/bases/project-overview.base` 会自动聚合这些入口。

不需要长期维护的临时资料，不放入 Projects。
