---
type: codex-project-bridge
status: active
project: Example Project
local_root: "<your-project-path>"
kb_project: "10-Projects/01-example-project/README.md"
startup_files:
  - "START-HERE.md"
  - "10-Projects/01-example-project/current-state.md"
  - "10-Projects/01-example-project/decisions.md"
---

# Codex 项目桥接卡｜Example Project

## 一句话定位

这是一个示例项目，演示 AI 如何从 Obsidian vault 接手项目、读取状态、执行任务并写回结果。

## 本地项目

| 项目 | 内容 |
|---|---|
| 本地路径 | `<your-project-path>` |
| 项目规则 | `AGENTS.md` 或项目 README |
| 知识库入口 | `10-Projects/01-example-project/README.md` |
| 当前状态 | `current-state.md` |
| 稳定决策 | `decisions.md` |

## 开工必读

1. `START-HERE.md`
2. 本桥接卡
3. `current-state.md`
4. `decisions.md`

## 当前状态

- 项目处于示例状态，未绑定真实业务。
- 可用于复制出真实项目桥接卡。

## 最近决策

- 公开版只放脱敏示例。
- 项目桥接卡只记录长期有效的状态和边界。
- 临时过程写交接卡，不写进桥接卡。

## 下次开工

- 复制本文件。
- 替换项目名、本地路径、当前状态和开工必读。
- 确认任务结束后写回位置。

## 可沉淀经验

- 如果同类项目会重复出现，把经验上浮到 `20-SharedAssets/02-modules/`。

## 写回规则

| 内容 | 写回位置 |
|---|---|
| 项目长期状态 | 本桥接卡或 `current-state.md` |
| 稳定决策 | `decisions.md` |
| 临时交接 | `01-Inbox/agent-handoffs/` |
| 可复用经验 | `20-SharedAssets/02-modules/` |
