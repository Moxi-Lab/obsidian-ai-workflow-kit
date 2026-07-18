---
type: recall-index
status: active
---

# Recall System

这一层告诉 AI：不同任务开始前应该读什么，而不是每次扫描整个 vault。

## 召回对象

| 对象 | 作用 |
|---|---|
| 项目桥接卡 | 当前状态、边界、写回位置 |
| 当前状态页 | 最近进展和下一步 |
| 决策页 | 稳定决定和原因 |
| 经验资产 | 反复出现的问题和解决方案 |
| 资料分析卡 | 外部资料的摘要和可用结论 |
| 召回字段 | 帮 AI 判断一页内容何时该读 |

## 文件

| 文件 | 用途 |
|---|---|
| `00-AI/recall/task-to-context-map.md` | 按任务类型列出必读上下文 |
| `00-AI/recall/recall-fields.md` | 说明召回字段怎么写 |
| `00-AI/recall/example-recall-chain.md` | 展示一次经验如何被后续任务召回 |
