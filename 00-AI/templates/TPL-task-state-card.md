---
type: local-task
created: {{date}}
updated: {{date}}
aliases: ["TPL-任务状态卡", "任务状态卡模板", "Task State Card Template"]
task_id: ""
title: ""
project: ""
priority: medium # low / medium / high
status: queued # queued / active / blocked / done / archived
depends_on: []
definition_of_done: []
next_action: ""
blocker: ""
evidence_links: []
---

# 任务状态卡：{{title}}

## 任务目标

- {{goal}}

> 只有任务需要排队、跨会话继续或等待外部条件时才创建本卡；当前对话可以完成的任务直接执行。

## 当前状态

- `status`: {{status}}
- `next_action`: {{next_action}}
- `updated`: {{date}} {{time}}

## 执行记录（只写关键变更）

- [{{time}}] `queued -> active`：
- [{{time}}] `active -> blocked`：
- [{{time}}] `blocked -> active`：
- [{{time}}] `active -> done`：

## 阻塞信息（仅 blocked 填写）

- blocker:
- 需要谁处理:
- 建议处理路径:

## 验收对齐（done 前必填）

- [ ] DoD-1：
- [ ] DoD-2：
- [ ] DoD-3：

## 证据链接

- {{evidence_link}}
