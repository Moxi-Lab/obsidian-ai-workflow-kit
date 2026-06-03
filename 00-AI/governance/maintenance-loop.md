---
type: governance-rule
status: active
---

# Maintenance Loop

知识库维护不是整理更多目录，而是让 AI 能继续找得到、信得过、用得上。

## 每周轻量维护

1. 运行：

```bash
python3 00-AI/scripts/kb.py health-check
```

2. 检查 `01-Inbox/` 是否有长期滞留。
3. 检查项目桥接卡是否仍然反映当前状态。
4. 检查高价值问答是否已沉淀成经验资产。
5. 检查召回地图是否能回答“这个任务开始前读什么”。

## 每月维护

- 合并重复资料卡。
- 标注过时结论。
- 把高复用经验挂到 `00-AI/recall/task-to-context-map.md`。
- 清理没有来源、没有结论、没有使用场景的临时内容。

