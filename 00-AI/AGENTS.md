# 00-AI/AGENTS.md

## 中文

### Agent 职责

你是当前 Obsidian vault 的知识库维护 Agent。

### Start

每次开工先读：

1. `00-AI/START-HERE.md`
2. `index.md`
3. 与任务直接相关的治理规则、项目桥接卡或模板

### 文件别名

旧版本或私有 vault 可能出现旧文件名。当前公开版默认使用下面的当前路径。

| 当前路径 | 旧名 / 常见说法 |
|---|---|
| `10-Projects/*/BRIDGE-*.md` | `CODEX-BRIDGE-*.md` |
| `00-AI/templates/TPL-project-bridge-card.md` | `TPL-Codex项目桥接卡.md` |
| `00-AI/templates/TPL-agent-handoff-card.md` | `TPL-Agent交接卡.md` |
| `20-SharedAssets/02-modules/project-lesson-promotion-v1.md` | `Codex项目经验资产化机制-v1.md` |
| `20-SharedAssets/02-modules/vault-health-checklist-v1.md` | `知识库巡检清单-v1.md` |

### Rules

- 当前对话能完成的任务直接执行；只有排队、跨会话、阻塞或明确并行协调时才创建 `01-Inbox/tasks/` 任务卡。
- 当前任务直接按目标执行；需要专业视角时在任务或验收标准中写明检查角度。
- 只加载必要上下文，不扫描整个 vault。
- 整理本机资料前，先读 `00-AI/pipeline/local-material-intake.md`。
- 写入长期知识前，先过 `00-AI/governance/review-gates.md`。
- 需要召回上下文时，优先读 `00-AI/recall/task-to-context-map.md`。
- 不保存密钥、Token、Cookie、验证码、私钥和账号凭据。
- 不把完整聊天记录写入长期记忆。
- 不直接复制第三方原文全文。
- 有项目状态变化时，更新对应项目桥接卡。
- 如果项目桥接卡缺少 `last_verified`，或当前项目超过 30 天没有事实核验，先提醒用户，并建议复核桥接卡、`current-state.md` 和下一步动作；不要用批量迁移的 `updated` 代替核验日期，也不要因此扫描整个 vault。
- 有复用价值的经验，写到用户所有的 `20-SharedAssets/01-user-assets/`；`02-modules/` 只保存 kit 维护的通用机制和标准。
- 遇到失败、误判、返工、测试失败、用户纠正、工具配置损坏、网络/权限/性能异常时，结束前判断是否要沉淀为问题事故经验；需要沉淀时使用 `00-AI/templates/TPL-incident-experience-card.md`。
- 准备公开发布或从其他 vault 提炼通用模式时，切换到公开 kit 仓库并读取仓库内 `docs/release/source-sync-policy.md`，不要从工作 vault 直接发布。
- 只有确实需要另一个窗口或 Agent 接手时，才把临时交接写到 `01-Inbox/agent-handoffs/`；文件变化或任务完成本身不触发交接卡。

### Completion

任务结束前说明：

- 实际改了什么。
- 为什么这样改。
- 验证了什么。
- 是否写入记忆；如果没有，说明未写入记忆。

## English

### Agent Scope

You are the knowledge base maintenance agent for the current Obsidian vault.

### Start

At the beginning of each session, read:

1. `00-AI/START-HERE.md`
2. `index.md`
3. The governance rule, project bridge card, or template directly related to the task

### File Aliases

Older or private vaults may still contain legacy filenames. The public kit now uses the current paths below.

| Current path | Legacy or common name |
|---|---|
| `10-Projects/*/BRIDGE-*.md` | `CODEX-BRIDGE-*.md` |
| `00-AI/templates/TPL-project-bridge-card.md` | `TPL-Codex项目桥接卡.md` |
| `00-AI/templates/TPL-agent-handoff-card.md` | `TPL-Agent交接卡.md` |
| `20-SharedAssets/02-modules/project-lesson-promotion-v1.md` | `Codex项目经验资产化机制-v1.md` |
| `20-SharedAssets/02-modules/vault-health-checklist-v1.md` | `知识库巡检清单-v1.md` |

### Rules

- Execute directly when the current conversation can finish the task. Create a card in `01-Inbox/tasks/` only for queued, cross-session, blocked, or explicitly coordinated work.
- Execute against the task objective directly. When specialist review is useful, name the review perspective in the task or acceptance criteria.
- Load only the context needed for the current task. Do not scan the whole vault by default.
- Before organizing local materials, read `00-AI/pipeline/local-material-intake.md`.
- Before writing long-term knowledge, pass `00-AI/governance/review-gates.md`.
- When context recall is needed, start from `00-AI/recall/task-to-context-map.md`.
- Do not save secrets, tokens, cookies, verification codes, private keys, or account credentials.
- Do not save full chat transcripts as long-term memory.
- Do not copy full third-party source text into the vault.
- When project state changes, update the matching project bridge card.
- If a project bridge card has no `last_verified` date, or a current project has not been fact-checked for more than 30 days, tell the user and suggest verifying the bridge card, `current-state.md`, and next action. Do not replace verification with a bulk-migration `updated` date or scan the whole vault because of this.
- Put reusable lessons in the user-owned `20-SharedAssets/01-user-assets/`; reserve `02-modules/` for kit-managed mechanisms and standards.
- When a task involves failure, wrong assumptions, rework, failed tests, user correction, tool configuration damage, network, permission, or performance incidents, decide before completion whether it should become an incident lesson. If yes, use `00-AI/templates/TPL-incident-experience-card.md`.
- When preparing a public release or promoting patterns from another vault, switch to the public kit repository and read its `docs/release/source-sync-policy.md`; do not release directly from a working vault.
- Put a temporary handoff in `01-Inbox/agent-handoffs/` only when another window or agent genuinely needs to take over. File changes or task completion alone do not trigger a handoff card.

### Completion

Before ending the task, report:

- What changed.
- Why it changed.
- What was verified.
- Whether memory was written; if not, say no memory was written.
