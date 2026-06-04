---
type: entry
status: active
aliases: ["入口", "开工入口", "Start Here"]
language: zh-CN
---

# START HERE

语言：中文

> 给任何新窗口 / 新 Agent：先读完本文件，就知道该读什么、写到哪里、不能做什么。

## 一句开工指令

```text
你是知识库维护 Agent，请阅读当前 vault 的 00-AI/START-HERE.md，并按里面的开工流程执行。
```

如果 AI 不是从 vault 根目录启动，把 vault 路径一并发给它：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<your-vault-path>。请先读取该目录下的 00-AI/START-HERE.md，并按里面的开工流程执行。
```

## 正确触发后的回执

AI 读完本文件后，应先用下面格式回执，而不是立刻扫描整个 vault：

```text
已读取：00-AI/START-HERE.md
任务类型：<整理本机资料 / 接手项目 / 整理外部资料 / 沉淀经验 / 维护知识库 / 写交接 / 待确认>
下一步先读：<具体文件>
结果写回：<具体目录或文件>
不会做：<本轮明确不做的事>
```

## 开工三步

### 第 1 步：确认任务类型

| 任务类型 | 先读 |
|---|---|
| 整理本机资料 | `00-AI/pipeline/README.md`、`00-AI/pipeline/local-material-intake.md` |
| 接手项目 | `10-Projects/<项目>/BRIDGE-*.md` |
| 整理外部资料 | `40-ExternalSources/README.md`、`00-AI/templates/TPL-source-analysis-card.md` |
| 沉淀经验 | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`、`00-AI/templates/TPL-question-knowledge-experience-asset-card.md` |
| 复盘问题/事故 | `20-SharedAssets/02-modules/project-lesson-promotion-v1.md`、`00-AI/templates/TPL-incident-experience-card.md` |
| 维护知识库 | `00-AI/governance/maintenance-loop.md`、`20-SharedAssets/02-modules/vault-health-checklist-v1.md` |
| 写交接 | `00-AI/templates/TPL-agent-handoff-card.md` |

### 第 2 步：只加载必要上下文

- 先读 `index.md` 和本文件。
- 需要治理规则时读 `00-AI/governance/README.md`。
- 需要召回规则时读 `00-AI/recall/task-to-context-map.md`。
- 有项目任务时，只读对应项目桥接卡。
- 不要一上来扫描整个 vault。

### 第 3 步：按写回位置保存结果

| 内容 | 写到哪里 |
|---|---|
| 临时交接 | `01-Inbox/agent-handoffs/` |
| 临时派工 | `01-Inbox/dispatch-cards/` |
| 外部资料分析 | `40-ExternalSources/01-samples/` 或对应主题目录 |
| 项目状态 | 对应项目桥接卡 |
| 复用经验 | `20-SharedAssets/02-modules/` |
| 问题/事故经验 | 复制 `00-AI/templates/TPL-incident-experience-card.md` 后写入对应项目或共享资产 |
| 召回规则 | `00-AI/recall/` |
| 标准模板 | `00-AI/templates/` |

## 禁止事项

- 不保存密钥、Token、Cookie、验证码、私钥和账号凭据。
- 不把完整聊天记录当长期记忆。
- 不直接复制第三方原文全文。
- 不把 Inbox 当长期目录。
- 不在没有明确任务时批量重构目录。

## 任务结束前检查

- 说明实际改了什么。
- 说明为什么这样改。
- 说明验证了什么。
- 说明是否写入记忆；如果没有，说明未写入记忆。
