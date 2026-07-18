---
type: recall-rule
status: active
---

# Recall Fields

召回字段的目的不是给所有笔记打复杂标签，而是让 AI 快速判断“这页是否该读”。

## 推荐字段

```yaml
type:
status:
project:
themes: []
keywords: []
question_text:
applicable_to: []
canonical: false
source_refs: []
```

## 字段说明

| 字段 | 用途 |
|---|---|
| `type` | 判断页面类型 |
| `status` | 判断是否可用 |
| `project` | 关联项目 |
| `themes` | 稳定主题 |
| `keywords` | 搜索关键词 |
| `question_text` | 这页回答什么问题 |
| `applicable_to` | 哪类任务开始前应该读 |
| `canonical` | 是否是权威版本 |
| `source_refs` | 来源 |

## 使用边界

- 原始剪藏默认不写复杂召回字段。
- 提炼后的资料分析卡、问题知识卡、经验资产卡才补字段。
- 同一主题只保留一张 `canonical: true` 的权威卡。
