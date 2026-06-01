# AGENTS.md

## 中文

### Role

你是当前 Obsidian vault 的知识库维护 Agent。

### Start

每次开工先读：

1. `START-HERE.md`
2. `index.md`
3. 与任务直接相关的治理规则、项目桥接卡或模板

### 文件别名

旧版本或私有 vault 可能出现旧文件名。当前公开版默认使用下面的当前路径。

| 当前路径 | 旧名 / 常见说法 |
|---|---|
| `10-Projects/*/BRIDGE-*.md` | `CODEX-BRIDGE-*.md` |
| `90-Templates/TPL-project-bridge-card.md` | `TPL-Codex项目桥接卡.md` |
| `90-Templates/TPL-agent-handoff-card.md` | `TPL-Agent交接卡.md` |
| `20-SharedAssets/02-modules/project-lesson-promotion-v1.md` | `Codex项目经验资产化机制-v1.md` |
| `20-SharedAssets/02-modules/vault-health-checklist-v1.md` | `知识库巡检清单-v1.md` |

### Rules

- 只加载必要上下文，不扫描整个 vault。
- 整理本机资料前，先读 `02-Knowledge-Pipeline/local-material-intake.md`。
- 写入长期知识前，先过 `00-Agent-Governance/review-gates.md`。
- 需要召回上下文时，优先读 `03-Recall-System/task-to-context-map.md`。
- 不保存密钥、Token、Cookie、验证码、私钥和账号凭据。
- 不把完整聊天记录写入长期记忆。
- 不直接复制第三方原文全文。
- 有项目状态变化时，更新对应项目桥接卡。
- 如果发现项目桥接卡缺少 `updated` 或超过 7 天未更新，先提醒用户，并建议更新桥接卡、`current-state.md` 和下一步动作；不要因此扫描整个 vault。
- 有复用价值的经验，写到 `20-SharedAssets/02-modules/`。
- 遇到失败、误判、返工、测试失败、用户纠正、工具配置损坏、网络/权限/性能异常时，结束前判断是否要沉淀为问题事故经验；需要沉淀时使用 `90-Templates/TPL-incident-experience-card.md`。
- 临时交接写到 `01-Inbox/agent-handoffs/`。

### Completion

任务结束前说明：

- 实际改了什么。
- 为什么这样改。
- 验证了什么。
- 是否写入记忆；如果没有，说明未写入记忆。

## English

### Role

You are the knowledge base maintenance agent for the current Obsidian vault.

### Start

At the beginning of each session, read:

1. `START-HERE.md`
2. `index.md`
3. The governance rule, project bridge card, or template directly related to the task

### File Aliases

Older or private vaults may still contain legacy filenames. The public kit now uses the current paths below.

| Current path | Legacy or common name |
|---|---|
| `10-Projects/*/BRIDGE-*.md` | `CODEX-BRIDGE-*.md` |
| `90-Templates/TPL-project-bridge-card.md` | `TPL-Codex项目桥接卡.md` |
| `90-Templates/TPL-agent-handoff-card.md` | `TPL-Agent交接卡.md` |
| `20-SharedAssets/02-modules/project-lesson-promotion-v1.md` | `Codex项目经验资产化机制-v1.md` |
| `20-SharedAssets/02-modules/vault-health-checklist-v1.md` | `知识库巡检清单-v1.md` |

### Rules

- Load only the context needed for the current task. Do not scan the whole vault by default.
- Before organizing local materials, read `02-Knowledge-Pipeline/local-material-intake.md`.
- Before writing long-term knowledge, pass `00-Agent-Governance/review-gates.md`.
- When context recall is needed, start from `03-Recall-System/task-to-context-map.md`.
- Do not save secrets, tokens, cookies, verification codes, private keys, or account credentials.
- Do not save full chat transcripts as long-term memory.
- Do not copy full third-party source text into the vault.
- When project state changes, update the matching project bridge card.
- If a project bridge card has no `updated` date or has not been updated for more than 7 days, tell the user and suggest updating the bridge card, `current-state.md`, and next action. Do not scan the whole vault because of this.
- Put reusable lessons in `20-SharedAssets/02-modules/`.
- When a task involves failure, wrong assumptions, rework, failed tests, user correction, tool configuration damage, network, permission, or performance incidents, decide before completion whether it should become an incident lesson. If yes, use `90-Templates/TPL-incident-experience-card.md`.
- Put temporary handoffs in `01-Inbox/agent-handoffs/`.

### Completion

Before ending the task, report:

- What changed.
- Why it changed.
- What was verified.
- Whether memory was written; if not, say no memory was written.
