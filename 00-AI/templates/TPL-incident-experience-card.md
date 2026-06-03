---
type: template
status: active
aliases: ["TPL-问题事故经验卡", "事故经验卡模板", "问题复盘模板", "Incident Experience Template"]
---

# TPL｜问题事故经验卡

> 用法：用于失败、误判、返工、测试失败、用户纠正、工具配置损坏、网络/权限/性能异常。目的不是记录过程，而是让下一位 AI 少踩同一个坑。

```yaml
---
id: INC-YYYYMMDD-001
type: incident-experience
title: ""
status: draft # draft / active / archived
project: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD

severity: medium # low / medium / high
source_refs: [] # handoff card, issue, log, file, or short source summary
themes: [] # e.g. agent-governance, web-clipper, deployment, permissions
keywords: []
applicable_to: [] # which future tasks should read this first
canonical: true
relationships: [] # related bridge cards, rules, or lessons
---
```

## 现象 / Symptom

- 用户或系统看到的问题：
-

## 影响 / Impact

- 造成了什么返工、风险或误判：
-

## 根因 / 稳定判断

- 已确认：
-
- 尚不确定：
-

## 触发条件 / Recall Trigger

- 下次看到什么现象时，应该想起这条经验：
-

## 处理动作 / Action

1.

## 验证方式 / Verification

- 怎么确认处理有效：
-

## 禁止事项 / Do Not

- 哪些动作容易扩大问题：
-

## 写回位置 / Write-back

- 项目桥接卡是否需要挂到“经验召回”：
-
- 是否需要变成检查清单 / SOP / skill：
-

## 复用记录 / Reuse Log

- YYYY-MM-DD：用于哪个项目 / 任务，结果如何。
