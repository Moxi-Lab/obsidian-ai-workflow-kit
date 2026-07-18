---
asset: true
asset_group: 规则资产
asset_label: 元数据最小标准
type: standard
aliases: ["元数据最小标准-v1", "Minimal Metadata Standard"]
created: 2026-05-14
updated: 2026-07-18
status: active
scope: cross-project
owner: maintainer
---

# 元数据最小标准 v1

## 目的

让 AI 能稳定判断一页内容的类型、状态、所属项目、更新时间和可用范围。

## 新增页面必填

```yaml
---
type:
created:
updated:
status:
---
```

## 字段说明

| 字段 | 含义 | 示例 |
|---|---|---|
| `type` | 页面类型 | `project-state`、`source-analysis`、`experience-asset`、`sop` |
| `created` | 创建日期 | `2026-05-14` |
| `updated` | 最近更新日期 | `2026-05-14` |
| `status` | 当前状态 | `active`、`draft`、`waiting`、`paused`、`archived` |

## status 按页面类型取值

`status` 不是全库通用标签。先判断页面类型，再从对应值域选择：

| 页面类型 | 合法状态 |
|---|---|
| 规则、资产、入口 | `draft / active / deprecated / historical` |
| 项目、项目桥接 | `active / waiting / paused / blocked / done / archived` |
| 外部资料、分析卡、剪藏 | `inbox / filed / processed / rejected` |
| 本地任务 | `queued / active / blocked / done / archived` |
| 交接卡 | `open / blocked / done / archived` |
| 验收与审核 | `pending / accepted / deferred / skipped` |

Frontmatter 使用未加引号的小写值，例如 `status: active`。不要用项目的 `done` 表示资料已处理，也不要把任务的 `queued` 写到项目页。

## 可复用资产补充字段

```yaml
asset: true
asset_group:
asset_label:
scope:
owner:
```

## 项目页补充字段

```yaml
project:
pillar:
project_entry:
priority:
stage:
last_verified:
next_action:
stage:
priority:
next_action:
```

每个长期项目只选择一页作为权威入口，并设置 `project_entry: true`。入口页必须同时填写 `type / updated / status / pillar / project / priority / stage / last_verified / next_action`。`priority` 使用 `p0 / p1 / p2 / p3`；`last_verified` 表示项目状态最近一次经过事实核验的日期，不能用批量迁移日期代替。普通 README、决策页、任务卡、模板和复盘不得设置 `project_entry: true`。

## 外部资料补充字段

```yaml
source:
author:
captured:
related_project:
related_notes:
```

`captured` 是公开版资料进入知识库的日期，也是资料 Base 的索引字段；通过 `intake-source` 或 `intake-folder` 创建的资料卡必须填写。

## 本地任务补充字段

```yaml
type: local-task
created:
updated:
status: queued
project:
priority: medium
next_action:
blocker:
```

只有排队、跨会话、阻塞或明确协调的任务才建卡。当前对话能够完成的工作直接执行。

## Web Clipper 原始剪藏补充字段

模板见 `00-AI/templates/TPL-web-clip-minimal.md`。原始剪藏只负责收进来和等待分拣，不直接承载长期结论。

```yaml
type: web-clip
status: inbox
source_platform:
tags:
  - clippings
themes: []
related_project:
canonical: false
```

## 问题知识卡 / 经验资产补充字段

用于高复用经验、外部资料提炼、内容选题沉淀、复杂项目关键经验。模板见 `00-AI/templates/TPL-question-knowledge-experience-asset-card.md`。

```yaml
id:
title:
source_refs:
source_authors:
themes:
keywords:
question_text:
question_type:
applicable_to:
canonical:
relationships:
```

| 字段 | 含义 |
|---|---|
| `question_text` | 这张卡回答的真实问题 |
| `applicable_to` | 哪类任务开始前应该读 |
| `source_refs` | 来源文件、链接、交接卡或 Issue |
| `themes` | 稳定主题，用于聚合 |
| `canonical` | 是否为权威卡，避免重复来源抢占入口 |

## 交接卡补充字段

```yaml
source_context:
rule_version:
handoff_type:
next_action:
links:
```

## 执行口径

- 新增页面必须满足本标准。
- 旧页面不做一次性批量补齐；只在被编辑时顺手补齐。
- 历史归档页可以保留旧格式。
- 状态不确定时使用该页面类型允许的保守值：项目用 `waiting`、资料用 `inbox`、任务用 `queued`、审核用 `pending`。不要写不在枚举中的 `unknown`，也不要凭空判断。
