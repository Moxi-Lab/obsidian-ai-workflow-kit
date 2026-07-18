# 核心概念

这页保存原本放在 README 里的详细说明，避免首页太长。

## 它解决什么问题

AI Agent 越常用，“换窗口就失忆”的问题越明显。现有方案大多绑在某个工具里，要么需要额外基础设施，要么只是全文检索，人和 AI 都很难共同维护。

这个仓库做的事，是在 Obsidian 这个本地知识文件系统上，加一层 AI 可读、可执行、可维护的操作约定。

| 方案 | 本质 | 缺陷 |
|---|---|---|
| Claude Code memory files | 工具内置记忆 | 绑定单一工具和工作流 |
| Cursor Rules | 项目级指令 | 更偏代码项目，不覆盖资料、经验和知识库维护 |
| 向量记忆系统 | 嵌入式记忆存储 | 需要基础设施，不透明，不方便人工编辑 |
| 普通 Obsidian / Notion 笔记 | 人类笔记 | AI 不知道入口、优先级和写回规则 |
| RAG 插件 | 全文检索 | 召回容易噪声大，缺少任务映射和优先级 |
| 这个仓库 | AI 可执行的 Obsidian 操作约定 | 本地文件、人类可编辑、工具无关、按任务召回 |

## 核心思路

### 1. 唯一入口

`00-AI/START-HERE.md` 会告诉 AI 当前是什么任务、先读哪些文件、结果应该写回哪里。

### 2. 资料整理流水线

`00-AI/pipeline/` 告诉 AI 如何进入本机资料、分类、提炼、连接、升舱和维护。

### 3. AI 治理层

`00-AI/governance/` 告诉 AI 哪些能写、写入前要验证什么、什么时候应该停止猜测。

### 4. 召回系统

`00-AI/recall/` 把任务类型映射到 AI 应该先读的文件。

### 5. 项目桥接卡

每个重要项目都有一张桥接卡，记录项目路径、当前状态、最近决策、下一步动作和写回规则。

可以从这个示例开始：

```text
10-Projects/01-example-project/BRIDGE-example.md
```

### 6. Inbox 只是临时区

`01-Inbox/` 用来接收交接卡、任务卡和网页剪藏，不作为长期保存目录。

当前对话是默认执行上下文。只有任务需要排队、跨会话、等待外部条件或明确协调时，才写入 `01-Inbox/tasks/`。默认流程不分配 CEO、CTO、QA 等岗位角色。

### 7. 经验要变成资产

重复出现的经验应该进入 `20-SharedAssets/`，并写清楚触发条件、处理动作和验证方式。

失败、误判、返工、测试失败、用户纠正和工具异常，如果能避免下次重复踩坑，就应该沉淀成问题事故经验。

### 8. 默认本地优先

这套结构适合复制到你自己的本地 Obsidian vault 中使用。真实项目状态、个人笔记、交接历史和私有资料都留在你自己的机器上。

### 9. Markdown 是事实源，Bases 是视图

Full 模式使用 Obsidian 自带的 Bases 提供项目、任务和资料动态视图。`project_entry`、类型化 `status`、`pillar` 和 `captured` 是索引字段，由只读健康检查守护。Base 不替代权威 Markdown 页面。

## 范围边界

这套结构只聚焦四件事：

- 资料流水线：把本地资料整理成结构化笔记。
- AI 治理：约束 AI 读什么、写什么、验证什么、避免什么。
- 召回系统：让 AI 按任务找到该读的上下文。
- 维护循环：让知识库持续保持健康。

它不是 RAG 系统，不是云服务，也不是托管任务管理器。它是一套本地优先的 Obsidian + AI 工作方法。

## 示例工作流

```text
用户指令
  -> 00-AI/START-HERE.md
  -> 召回地图
  -> 治理规则
  -> 资料流水线或项目桥接卡
  -> 结构化写回
  -> 可复用经验进入召回系统
```

可以查看演示：

```text
examples/ai-handoff-demo/README.md
```

想看更接近真实使用状态的填充示例：

```text
examples/filled-example/
```

想看一条资料如何从原始输入变成可召回知识：

```text
examples/source-to-knowledge/
```

日常使用不需要读完整仓库：初始化之后，大多数 AI 会话只需要读 `00-AI/START-HERE.md`、一个项目桥接卡，以及该项目的 `current-state.md` / `decisions.md`。

如果你已经有自己的 Obsidian vault，先看 [迁移指南](migration.md)。不要重建整个 vault，先加一张项目桥接卡。

## 仓库结构

| 路径 | 作用 |
|---|---|
| [`00-AI/START-HERE.md`](../00-AI/START-HERE.md) | AI Agent 第一个应该读的文件 |
| [`index.md`](../index.md) | 给人看的 vault 首页 |
| [`00-AI/AGENTS.md`](../00-AI/AGENTS.md) | 给 Claude Code、Cursor、Codex 等 AI agent 的规则 |
| [`00-AI/governance/`](../00-AI/governance/) | 开工契约、审查门、写回规则、维护循环 |
| [`01-Inbox/`](../01-Inbox/) | 临时交接、排队或跨会话任务卡、网页剪藏入口 |
| [`00-AI/pipeline/`](../00-AI/pipeline/) | AI 如何把本机资料整理成结构化知识 |
| [`00-AI/recall/`](../00-AI/recall/) | 任务到上下文的召回地图和召回字段 |
| [`00-AI/bases/`](../00-AI/bases/) | Full 模式安装的项目、任务和资料动态视图 |
| [`10-Projects/`](../10-Projects/) | 项目工作区和项目桥接卡 |
| [`20-SharedAssets/`](../20-SharedAssets/) | 可复用方法、SOP 和工作流 |
| [`40-ExternalSources/`](../40-ExternalSources/) | 外部资料分析卡，不保存第三方全文 |
| [`00-AI/templates/`](../00-AI/templates/) | 标准模板 |
| [`docs/`](./) | 首次体验指南、架构图和面向使用者的说明文档 |
| [`00-AI/scripts/`](../00-AI/scripts/) | 创建项目卡和巡检的轻量脚本 |
| [`examples/`](../examples/) | 从开工到交接的完整示例 |

核心文件名已统一为英文，方便英文 AI Agent 按路径读取；页面标题和部分正文保留中文，用来保留原始工作方法。
