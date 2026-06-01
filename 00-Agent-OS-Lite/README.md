---
type: agent-os-readme
status: active
---

# Agent OS Lite

这里放给 AI 使用的最小工作规则。它的目标不是做完整的 Agent 管理系统，而是让任意新 Agent 进入 vault 后能快速知道：从哪里开始、读哪些文件、结果写回哪里。

## Lite 的边界

这个公开版只保留四类东西：

- 一页纸开工规则：`00-entry/one-page-rules.md`
- 核心规则索引：`10-rules/README.md`
- 项目登记表：`20-registries/PROJECTS-REGISTRY.md`
- 巡检报告样例：`30-run-reports/HEALTH-CHECK-SAMPLE.md`

不包含：

- 角色系统、员工手册或组织管理流程。
- 长期运行日志。
- 自动任务调度。
- 私有项目状态。

完整私有库可以有更复杂的 Agent OS；这个 Lite 版只保留开源 starter kit 必要的工作边界。

## 与 SharedAssets 的关系

`00-Agent-OS-Lite/` 只放“开工怎么做”的最小规则。可复用方法、SOP、巡检清单和经验资产放在 `20-SharedAssets/`。

判断标准：

| 内容 | 放置位置 |
|---|---|
| AI 每次开工都要遵守的规则 | `00-Agent-OS-Lite/` |
| 可复用方法、SOP、检查清单 | `20-SharedAssets/` |
| 项目状态和决策 | `10-Projects/` |
| 临时交接和派工 | `01-Inbox/` |

## 目录

| 路径 | 作用 |
|---|---|
| `00-entry/` | 入口和一页纸规则 |
| `10-rules/` | 核心规则索引 |
| `20-registries/` | 项目登记表 |
| `30-run-reports/` | 巡检报告样例 |
