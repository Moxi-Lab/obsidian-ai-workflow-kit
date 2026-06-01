---
type: entry
status: active
aliases: ["入口", "开工入口", "Start Here"]
---

# START HERE

> 给任何新窗口 / 新 Agent：读完本文件，就知道自己该读什么、该写到哪里、不能做什么。

## 一句开工指令

中文：

```text
你是知识库维护 Agent，请阅读当前 vault 的 START-HERE.md，并按里面的开工流程执行。
```

English:

```text
You are the knowledge base maintenance agent. Read START-HERE.md in the current vault and follow its startup workflow.
```

如果 AI 不是从 vault 根目录启动，把 vault 路径一并发给它：

中文：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<your-vault-path>。请先读取该目录下的 START-HERE.md，并按里面的开工流程执行。
```

English:

```text
You are the knowledge base maintenance agent. The root directory of this Obsidian vault is: <your-vault-path>. First read START-HERE.md in that directory, then follow its startup workflow.
```

## 正确触发后的回执

AI 读完本文件后，应先用下面格式回执，而不是立刻扫描整个 vault：

```text
已读取 START-HERE.md
任务类型：<接手项目 / 整理外部资料 / 沉淀经验 / 维护知识库 / 写交接 / 待确认>
下一步先读：<具体文件>
结果写回：<具体目录或文件>
```

## 开工三步

### 第 1 步：确认任务类型

| 任务类型 | 先读 |
|---|---|
| 接手项目 | `10-Projects/<项目>/CODEX-BRIDGE-*.md` |
| 整理外部资料 | `40-ExternalSources/README.md`、`90-Templates/TPL-资料分析卡.md` |
| 沉淀经验 | `20-SharedAssets/02-modules/Codex项目经验资产化机制-v1.md` |
| 维护知识库 | `20-SharedAssets/02-modules/知识库巡检清单-v1.md` |
| 写交接 | `90-Templates/TPL-Agent交接卡.md` |

### 第 2 步：只加载必要上下文

- 先读 `index.md` 和本文件。
- 有项目任务时，只读对应项目桥接卡。
- 有外部资料时，只读资料分析模板和相关项目页。
- 不要一上来扫描整个 vault。

### 第 3 步：按写回位置保存结果

| 内容 | 写到哪里 |
|---|---|
| 临时交接 | `01-Inbox/agent-handoffs/00-Inbox/` |
| 临时派工 | `01-Inbox/dispatch-cards/00-Inbox/` |
| 外部资料分析 | `40-ExternalSources/01-samples/` 或对应主题目录 |
| 项目状态 | 对应项目桥接卡 |
| 复用经验 | `20-SharedAssets/02-modules/` |
| 标准模板 | `90-Templates/` |

## 当前示例项目

| 项目 | 桥接卡 | 用途 |
|---|---|---|
| Example Project | `10-Projects/01-example-project/CODEX-BRIDGE-example.md` | 演示 AI 如何接手项目、读取状态、写回交接 |

## 禁止事项

- 不保存密钥、Token、Cookie、验证码、私钥和账号凭据。
- 不把完整聊天记录当长期记忆。
- 不直接复制第三方原文全文。
- 不把 Inbox 当长期目录。
- 不在没有明确任务时批量重构目录。

## 任务结束前检查

- 是否更新了项目桥接卡。
- 是否把临时资料移出 Inbox 或标明下一步。
- 是否有经验值得上浮到共享资产。
- 是否留下了下一次 AI 可以接手的入口。
