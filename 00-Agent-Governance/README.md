---
type: governance-index
status: active
---

# Agent Governance

这一层回答一个问题：AI 进入 vault 后，怎么少猜、少乱写、能维护。

它不是角色系统，也不是组织管理。它只定义 AI 管理本地知识库时必须遵守的四件事：

| 文件 | 作用 |
|---|---|
| `startup-contract.md` | 开工时先确认任务类型、必读文件和写回位置 |
| `write-back-rules.md` | 判断资料、项目状态、经验、临时交接应该写到哪里 |
| `review-gates.md` | 写入长期知识前必须做的检查 |
| `maintenance-loop.md` | 定期维护知识库健康的循环 |

## 核心原则

- AI 不直接扫描整个 vault。
- AI 不把原始聊天记录当长期知识。
- AI 不复制第三方全文。
- AI 写入长期知识前，要分清事实、判断和下一步动作。
- AI 结束任务前，要留下下一次能接手的入口。

