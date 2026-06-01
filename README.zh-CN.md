# Obsidian AI Memory Kit

中文 | [English](README.md)

别再每次都重新给 AI 解释你的项目。

如果你真的用 Obsidian 工作，你的 vault 里已经有 AI 需要的东西：项目上下文、关键决策、参考资料、踩坑经验、未完成线索。问题是，它们通常不是按“AI 接手”来组织的，所以每个新会话还是从零开始。

Obsidian AI Memory Kit 把这些私人知识整理成一层可复用的工作记忆，让 AI 不再像第一次来的临时助手，而更像一直跟着项目走的长期同事。

它能帮你：

- 少花时间给每次 AI 会话重新补上下文。
- 把项目决策、当前状态、下一步动作放到 AI 能稳定找到的位置。
- 把反复出现的解决方案和经验沉淀成可复用资产，而不是丢在聊天记录里。
- 下载后直接在自己的本地 Obsidian vault 里使用。
- 让 Obsidian 不只是笔记归档，而是人和 AI 长期协作的工作空间。

## Quick Start

1. 把这个仓库复制成一个新的 Obsidian vault。
2. 打开 `START-HERE.md`。
3. 把下面这句话发给你的 AI Agent：

中文：

```text
你是知识库维护 Agent，请阅读当前 vault 的 START-HERE.md，并按里面的开工流程执行。
```

English:

```text
You are the knowledge base maintenance agent. Read START-HERE.md in the current vault and follow its startup workflow.
```

如果你的 AI 不是从 vault 根目录启动，需要把 vault 路径一起发给它：

中文：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<your-vault-path>。请先读取该目录下的 START-HERE.md，并按里面的开工流程执行。
```

English:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read START-HERE.md in that directory, then follow its startup workflow.
```

用内置示例项目测试时，AI 应该能根据入口找到项目桥接卡，读取当前状态，完成任务，并把结果写回正确位置。

## 为什么需要它

大多数笔记是给人看的，但不一定适合 AI 稳定接手项目工作。

这套结构是在 Obsidian 上加一层轻量工作规则：

| 问题 | 这套结构提供什么 |
|---|---|
| AI 不知道从哪里开始 | 用 `START-HERE.md` 作为唯一开工入口 |
| 项目上下文散落各处 | 用 `10-Projects/` 里的项目桥接卡串起来 |
| 有用经验停留在聊天记录里 | 沉淀到 `20-SharedAssets/` |
| 临时资料越来越乱 | 用 `01-Inbox/` 做临时分流 |
| 外部资料容易整篇复制进库 | 用 `40-ExternalSources/` 做资料分析卡 |
| 每个 Agent 做法不一致 | 用 `AGENTS.md` 和 `00-Agent-OS-Lite/` 统一规则 |

## 仓库结构

```text
.
├── START-HERE.md
├── index.md
├── AGENTS.md
├── 00-Agent-OS-Lite/
├── 01-Inbox/
├── 02-MOCs/
├── 10-Projects/
├── 20-SharedAssets/
├── 40-ExternalSources/
├── 90-Templates/
└── examples/
```

| 路径 | 作用 |
|---|---|
| [`START-HERE.md`](START-HERE.md) | AI Agent 第一个应该读的文件 |
| [`index.md`](index.md) | 给人看的 vault 首页 |
| [`AGENTS.md`](AGENTS.md) | 给 Codex、Claude Code 等 coding agent 的规则 |
| [`00-Agent-OS-Lite/`](00-Agent-OS-Lite/) | 精简版 Agent 工作规则和登记表 |
| [`01-Inbox/`](01-Inbox/) | 临时交接、派工卡、网页剪藏入口 |
| [`02-MOCs/`](02-MOCs/) | 给人看的主题地图 |
| [`10-Projects/`](10-Projects/) | 项目工作区和项目桥接卡 |
| [`20-SharedAssets/`](20-SharedAssets/) | 可复用方法、SOP 和工作流 |
| [`40-ExternalSources/`](40-ExternalSources/) | 外部资料分析卡，不保存第三方全文 |
| [`90-Templates/`](90-Templates/) | 标准模板 |
| [`examples/`](examples/) | 从开工到交接的完整示例 |

## 核心思路

### 1. 唯一入口

`START-HERE.md` 会告诉 AI 当前是什么任务、先读哪些文件、结果应该写回哪里。

### 2. 项目桥接卡

每个重要项目都有一张桥接卡，记录项目路径、当前状态、最近决策、下一步动作和写回规则。

可以从这个示例开始：

```text
10-Projects/01-example-project/CODEX-BRIDGE-example.md
```

### 3. Inbox 只是临时区

`01-Inbox/` 用来接收交接卡、任务卡和网页剪藏，不作为长期保存目录。

### 4. 经验要变成资产

重复出现的经验应该进入 `20-SharedAssets/`，并写清楚触发条件、处理动作和验证方式。

### 5. 默认本地优先

这套结构适合复制到你自己的本地 Obsidian vault 中使用。真实项目状态、个人笔记、交接历史和私有资料都留在你自己的机器上。

## 示例工作流

```text
用户指令
  -> START-HERE.md
  -> 项目桥接卡
  -> 当前状态 / 决策记录
  -> 执行任务
  -> 写回项目或 Inbox
  -> 可复用经验进入 SharedAssets
```

可以查看演示：

```text
examples/ai-handoff-demo/README.md
```

## 内置模板

| 模板 | 用途 |
|---|---|
| [`TPL-Codex项目桥接卡.md`](90-Templates/TPL-Codex项目桥接卡.md) | 项目接手和接续 |
| [`TPL-Agent交接卡.md`](90-Templates/TPL-Agent交接卡.md) | 任务结束交接 |
| [`TPL-资料分析卡.md`](90-Templates/TPL-资料分析卡.md) | 外部资料分析 |
| [`TPL-任务状态卡.md`](90-Templates/TPL-任务状态卡.md) | 任务状态跟踪 |
| [`TPL-验收记录.md`](90-Templates/TPL-验收记录.md) | 验收记录 |
| [`TPL-问题知识卡-经验资产卡.md`](90-Templates/TPL-问题知识卡-经验资产卡.md) | 高复用问题和经验资产 |
| [`TPL-WebClip-最简模板.md`](90-Templates/TPL-WebClip-最简模板.md) | Web Clipper 原始剪藏 |

## 不包含什么

这个仓库有意排除了：

- 个人资料、偏好和真实项目状态。
- 第三方文章、X 帖、网页剪藏全文或长篇翻译。
- 交易记录、账户信息或策略运行状态。
- Agent 运行日志和私人交接历史。
- 本机路径、同步脚本、API Key、Token、Cookie、私钥、密码和验证码。

## License

- 原创文字内容：CC BY 4.0。
- 代码、脚本和可执行片段：MIT。
- 第三方内容不包含在本仓库授权范围内。
