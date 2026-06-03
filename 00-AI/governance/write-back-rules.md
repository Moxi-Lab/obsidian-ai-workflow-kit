---
type: governance-rule
status: active
---

# Write-back Rules

AI 写入前先判断内容类型，再写到对应位置。

| 内容类型 | 写回位置 | 长期价值判断 |
|---|---|---|
| 项目长期状态 | `10-Projects/<project>/current-state.md` 或项目桥接卡 | 下次接手必须知道 |
| 稳定决策 | `10-Projects/<project>/decisions.md` | 已确认且会影响后续行动 |
| 临时交接 | `01-Inbox/agent-handoffs/` | 只服务下一次接续 |
| 外部资料分析 | `40-ExternalSources/` | 有来源、有摘要、有可用结论 |
| 可复用经验 | `20-SharedAssets/02-modules/` 或问题知识卡 | 未来多个任务会重复用 |
| 问题/事故经验 | 用 `00-AI/templates/TPL-incident-experience-card.md` 新建后放到项目或 `20-SharedAssets/02-modules/` | 下次能避免失败、误判、返工或工具异常 |
| 召回规则 | `00-AI/recall/` | 能告诉 AI 什么任务先读什么 |
| 模板 | `00-AI/templates/` | 会重复创建同类页面 |

## 写入格式

- 事实：写清来源。
- 判断：标明是推断还是已验证结论。
- 下一步：写成可执行动作。
- 风险：写清楚不能做什么。
- 问题/事故：必须写清触发条件、根因、处理动作、验证方式和禁止事项。

## 删除规则

AI 默认不删除长期内容。确实需要删除时，先说明：

- 删除对象。
- 删除原因。
- 是否有替代入口。
- 是否会影响召回。
