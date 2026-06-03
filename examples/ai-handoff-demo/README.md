---
type: example
status: active
---

# AI 接手演示

## 场景

用户只给 AI 一句话：

```text
你是知识库维护 Agent，请阅读当前 vault 的 00-AI/START-HERE.md，并按里面的开工流程执行。
```

## AI 应该读到

1. `00-AI/START-HERE.md`
2. `index.md`
3. `10-Projects/01-example-project/BRIDGE-example.md`
4. `10-Projects/01-example-project/current-state.md`

## AI 应该输出

- 当前任务类型。
- 已读取的入口。
- 建议下一步。
- 结果写回位置。

## 结束写回

如果任务完成，写交接卡到：

`01-Inbox/agent-handoffs/`
