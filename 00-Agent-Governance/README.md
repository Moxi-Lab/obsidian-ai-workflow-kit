---
type: governance-index
status: active
---

# Agent Governance

## 中文

这一层回答一个问题：AI 进入 vault 后，怎么少猜、少乱写、能维护。

它不是角色系统，也不是组织管理。它只定义 AI 管理本地知识库时必须遵守的四件事：

| 文件 | 作用 |
|---|---|
| `startup-contract.md` | 开工时先确认任务类型、必读文件和写回位置 |
| `write-back-rules.md` | 判断资料、项目状态、经验、临时交接应该写到哪里 |
| `review-gates.md` | 写入长期知识前必须做的检查 |
| `maintenance-loop.md` | 定期维护知识库健康的循环 |

### 核心原则

- AI 不直接扫描整个 vault。
- AI 不把原始聊天记录当长期知识。
- AI 不复制第三方全文。
- AI 写入长期知识前，要分清事实、判断和下一步动作。
- AI 遇到失败、误判、返工、用户纠正或工具异常时，要判断是否沉淀成问题事故经验。
- AI 结束任务前，要留下下一次能接手的入口。

## English

This layer answers one question: after AI enters the vault, how does it avoid guessing, write safely, and keep the knowledge base maintainable?

It is not a role system or an organization chart. It defines four rules AI must follow when maintaining a local knowledge base:

| File | Use |
|---|---|
| `startup-contract.md` | Confirm task type, required files, and write-back target before work starts |
| `write-back-rules.md` | Decide where materials, project state, lessons, and temporary handoffs should go |
| `review-gates.md` | Check long-term knowledge before writing it |
| `maintenance-loop.md` | Run the recurring knowledge base health loop |

### Core Principles

- AI does not scan the whole vault by default.
- AI does not treat raw chat transcripts as long-term knowledge.
- AI does not copy full third-party source text.
- Before writing long-term knowledge, AI separates facts, judgment, and next actions.
- When AI hits failure, wrong assumptions, rework, user correction, or tool incidents, it checks whether an incident lesson should be promoted.
- Before ending a task, AI leaves an entry point that the next session can resume from.
