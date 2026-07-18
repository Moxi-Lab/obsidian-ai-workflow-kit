---
type: pipeline-workflow
status: active
---

# Source To Knowledge Workflow

这条流程用于把一份资料变成可召回知识。

## 1. 原始资料

记录：

- 来源标题。
- 原始路径或 URL。
- 作者或来源平台。
- 获取日期。
- 是否允许长期保存全文。

## 2. 资料分析卡

使用 `00-AI/templates/TPL-source-analysis-card.md`，只保留：

- 一句话摘要。
- 关键结论。
- 对当前项目的影响。
- 可复用动作。
- 来源链接。

## 3. 知识升舱

满足任一条件才升舱：

- 会被多个项目复用。
- 下次任务开始前必须召回。
- 能变成检查清单、模板或判断规则。
- 已经第二次出现。

升舱时不要移动或覆盖原资料分析卡。原卡继续留在 `40-ExternalSources/` 作为来源证据，保持 `canonical: false`。

升舱后的写入位置：

| 价值类型 | 写入位置 |
|---|---|
| 影响某个项目状态 | `10-Projects/<project>/current-state.md` |
| 形成稳定项目决策 | `10-Projects/<project>/decisions.md` |
| 可被多个项目复用 | 用 `00-AI/templates/TPL-question-knowledge-experience-asset-card.md` 新建卡片，或写入 `20-SharedAssets/01-user-assets/` |
| 以后任务开始前必须召回 | 更新对应项目桥接卡，或更新 `00-AI/recall/task-to-context-map.md` |

只有升舱后的权威卡或共享资产才设置 `canonical: true`。

## 4. 召回挂载

高价值内容必须挂到：

- 对应项目桥接卡。
- `00-AI/recall/task-to-context-map.md`。

否则它只是“保存了”，不是“可召回”。
