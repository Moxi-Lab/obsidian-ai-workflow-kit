---
asset: true
asset_group: 规则资产
asset_label: 标签与召回字段设计
type: standard
aliases: ["标签与召回字段设计-v1", "Tag and Recall Field Design"]
created: 2026-06-01
updated: 2026-06-01
status: active
scope: cross-project
owner: maintainer
---

# 标签与召回字段设计 v1

## 目的

让 AI 能用少量稳定字段判断一页内容是否值得读取，而不是靠全库扫描或给所有文件批量打复杂标签。

## 核心原则

- 不照搬外部问题库标签体系。
- 不做全库批量迁移。
- 保留基础元数据：`type`、`status`、`project`、`themes`。
- 只给高价值卡片补召回字段。
- 原始剪藏只负责进入和分拣，不直接承载长期结论。

## 哪些内容需要召回字段

| 内容 | 是否需要 |
|---|---|
| 高复用经验 | 需要 |
| 外部资料提炼后的稳定结论 | 需要 |
| 内容选题沉淀 | 需要 |
| 复杂项目关键经验 | 需要 |
| 普通流水记录 | 不需要 |
| 临时状态 | 不需要 |
| 一次性聊天结论 | 不需要 |
| Web Clipper 原始剪藏 | 不需要 |

## 召回字段

用于 `00-AI/templates/TPL-question-knowledge-experience-asset-card.md`：

```yaml
source_refs: []
source_authors: []
themes: []
keywords: []
question_text: ""
question_type: ""
applicable_to: []
canonical: true
relationships: []
```

| 字段 | 作用 |
|---|---|
| `question_text` | 这张卡回答的真实问题 |
| `applicable_to` | 哪类任务开始前应该读 |
| `source_refs` | 来源文件、链接、交接卡或 Issue |
| `themes` | 稳定主题，用于聚合 |
| `canonical` | 是否为权威卡，避免重复来源抢占入口 |
| `relationships` | 相关卡片或项目桥接卡 |

## Web Clipper 标签口径

原始网页剪藏默认只保留来源和状态信息：

```yaml
type: web-clip
status: inbox
tags:
  - clippings
themes: []
canonical: false
```

不要在原始剪藏中填写 `question_text`、`applicable_to` 等召回字段。只有提炼后的问题知识卡或经验资产卡才使用这些字段。
