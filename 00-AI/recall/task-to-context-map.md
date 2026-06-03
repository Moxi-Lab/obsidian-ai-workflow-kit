---
type: recall-map
status: active
---

# Task To Context Map

AI 接到任务后，先用这张表决定读什么。

| 任务类型 | 必读 | 可选 |
|---|---|---|
| 整理本机资料 | `00-AI/pipeline/local-material-intake.md` | `00-AI/pipeline/source-to-knowledge-workflow.md` |
| 接手项目 | 对应项目桥接卡、`current-state.md`、`decisions.md` | 相关经验资产 |
| 整理外部资料 | `40-ExternalSources/README.md`、`00-AI/templates/TPL-source-analysis-card.md` | 对应项目桥接卡 |
| 沉淀经验 | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`、`00-AI/templates/TPL-question-knowledge-experience-asset-card.md` | 来源交接卡 |
| 复盘问题/事故 | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`、`00-AI/templates/TPL-incident-experience-card.md` | 来源交接卡、项目桥接卡、相关日志 |
| 维护知识库 | `00-AI/governance/maintenance-loop.md`、`20-SharedAssets/02-modules/vault-health-checklist-v1.md` | 最近健康报告 |
| 写交接 | `00-AI/templates/TPL-agent-handoff-card.md` | 项目桥接卡 |
| 理解召回链 | `00-AI/recall/example-recall-chain.md` | `examples/filled-example/BRIDGE-launch-notes.md` |

## 使用规则

- 首轮只读“必读”列。
- 只有任务需要时再读“可选”列。
- 新增高复用经验后，要补到对应任务类型。
- 如果项目桥接卡过期，先提醒用户，再继续短任务；长任务开始前建议更新桥接卡。
