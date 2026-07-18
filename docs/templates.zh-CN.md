# 模板说明

模板是可选的 Markdown 起点。当一条笔记需要变成后续 AI 会话可复用的上下文时，再使用模板。

| 模板 | 用途 |
|---|---|
| [`TPL-project-bridge-card.md`](../00-AI/templates/TPL-project-bridge-card.md) | 项目接手和接续 |
| [`TPL-agent-handoff-card.md`](../00-AI/templates/TPL-agent-handoff-card.md) | 任务结束交接 |
| [`TPL-source-analysis-card.md`](../00-AI/templates/TPL-source-analysis-card.md) | 外部资料分析 |
| [`TPL-task-state-card.md`](../00-AI/templates/TPL-task-state-card.md) | 任务状态跟踪 |
| [`TPL-acceptance-record.md`](../00-AI/templates/TPL-acceptance-record.md) | 验收记录 |
| [`TPL-question-knowledge-experience-asset-card.md`](../00-AI/templates/TPL-question-knowledge-experience-asset-card.md) | 高复用问题和经验资产 |
| [`TPL-incident-experience-card.md`](../00-AI/templates/TPL-incident-experience-card.md) | 失败、返工、误判和工具异常复盘 |
| [`TPL-web-clip-minimal.md`](../00-AI/templates/TPL-web-clip-minimal.md) | Web Clipper 原始剪藏 |

## 什么时候用

- 项目需要多次被 AI 接手时，用项目桥接卡。
- 工作确实需要换会话继续，而且项目桥接卡不足以承载临时状态时，才用 Agent 交接卡。
- 导入文件、文章、PDF 或网页资料时，用资料分析卡。
- 任务需要排队、跨会话继续或处于阻塞时，才用任务状态卡；当前对话可以完成就直接执行。
- 结果需要留下验证证据时，用验收记录。
- 某条经验后续会复用时，用问题知识卡 / 经验资产卡。
- 失败、误判、返工或工具问题能避免下次重复发生时，用问题事故经验卡。
- Web Clipper 只负责原始剪藏；后续有价值时再升舱。

默认任务模板把分流信息直接写在任务本身，包括目标、下一步、阻塞原因、优先级和验收证据。
