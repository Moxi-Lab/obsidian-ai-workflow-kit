# Obsidian AI Workflow Kit

中文 | [English](README.md)

[![CI](https://github.com/Moxi-Lab/obsidian-ai-workflow-kit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Moxi-Lab/obsidian-ai-workflow-kit/actions/workflows/ci.yml)

让你的本地 Obsidian vault 变成 AI 能读取、写回和维护的知识库。

你打开一个新的 Claude Code、Cursor、Codex 或 ChatGPT 会话。它又问你：这个项目是什么？关键资料在哪？上次做到哪？哪些内容不能乱改？

这套 kit 解决的就是这个接手问题：用一个本地优先的 Obsidian 结构，提供唯一开工入口、项目桥接卡、写回规则、资料分流、召回地图和维护检查。

它不是 App、插件、云端记忆服务，也不是 RAG 系统。它是一套文件系统层的工作流：人能直接改，任何能读取本地文件的 AI Agent 都能执行。

## 快速开始

### 安装到已有 vault

推荐第一步：先把最小层安装进你自己的 vault。

先预览：

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone --dry-run "/path/to/your-vault"
```

确认后安装：

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --mode barebone "/path/to/your-vault"
```

检查：

```bash
python3 "/path/to/your-vault/scripts/kb.py" health-check --vault "/path/to/your-vault" --mode barebone
```

然后把这句话发给你的 AI Agent：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<your-vault-path>。请先读取该目录下的 START-HERE.md，并按里面的开工流程执行。
```

如果你想安装完整 starter vault，包括资料流水线、召回系统、文档、示例和模板，使用默认 full 模式：

```bash
curl -fsSL https://raw.githubusercontent.com/Moxi-Lab/obsidian-ai-workflow-kit/main/install.sh | bash -s -- "/path/to/your-vault"
```

安装器默认跳过已有文件；只有你明确传入 `--overwrite` 才会覆盖。

### 当作演示 vault 打开

1. 克隆或下载这个仓库。
2. 在 Obsidian 里选择 **Open folder as vault**，打开这个仓库目录。
3. 打开 `START-HERE.md`。
4. 把上面的开工指令发给 AI。

不需要 Obsidian 社区插件。

## 你会得到什么

| 需求 | 对应结构 |
|---|---|
| AI 不知道从哪开始 | `START-HERE.md` |
| 项目上下文散落各处 | `10-Projects/` 里的项目桥接卡 |
| AI 写入太随意 | `00-Agent-Governance/` 里的治理规则 |
| 本机资料需要整理 | `02-Knowledge-Pipeline/` 里的资料流水线 |
| 有用经验难召回 | `03-Recall-System/` 里的任务地图和召回字段 |
| vault 越用越乱 | 健康检查和维护规则 |

## 它怎么工作

![Obsidian AI Workflow Kit 架构图](docs/images/architecture-flow.png)

日常使用保持很小：

```text
用户任务
  -> START-HERE.md
  -> 对应项目桥接卡或任务地图
  -> 只读取必要上下文
  -> 结构化写回
  -> 可复用经验进入后续召回
```

AI 默认不应该扫描整个 vault。它应该先读开工入口，再按任务映射打开必要上下文，完成任务后写回正确位置。

## 安装模式

| 模式 | 适合场景 | 会安装什么 |
|---|---|---|
| `barebone` | 给已有 vault 加一个最小入口 | 开工入口、治理规则、项目登记、项目桥接模板、`scripts/kb.py` |
| `full` | 新建 starter vault 或完整试用 | 全部工作流目录、示例、文档、模板、脚本 |

如果你不想用远程 `curl` 安装，可以本地克隆后运行：

```bash
bash install.sh --mode barebone --dry-run "/path/to/your-vault"
bash install.sh --mode barebone "/path/to/your-vault"
```

## 适合你吗？

适合：

- 你已经用 Obsidian 保存项目笔记、资料或决策。
- 你经常用 AI Agent，已经感受到换窗口后的上下文断层。
- 你想要本地优先、人工可编辑的 AI 记忆。
- 你愿意持续维护项目状态、交接和经验。

不适合：

- 你想要图形化 Obsidian 插件。
- 你想要云端记忆服务或托管 RAG 后端。
- 你想让 AI 自动扫描整台电脑。
- 你想自动批量改写已有 vault。

## 继续阅读

- [10 分钟首次体验](docs/10-minute-first-run.zh-CN.md)
- [Before / After 案例](docs/before-after-case.zh-CN.md)
- [自动化入门](docs/automation.zh-CN.md)
- [迁移指南](MIGRATION.md)
- [核心概念](docs/concepts.zh-CN.md)
- [模板说明](docs/templates.zh-CN.md)
- [脚本说明](scripts/README.md)
- [发布检查清单](RELEASE_CHECKLIST.md)

## 仓库结构

```text
START-HERE.md              AI 开工入口
00-Agent-Governance/       写回、审查和维护规则
02-Knowledge-Pipeline/     本机资料进入和升舱
03-Recall-System/          任务到上下文的召回地图
10-Projects/               项目工作区和项目桥接卡
20-SharedAssets/           可复用方法和经验
40-ExternalSources/        资料分析卡
90-Templates/              可复用笔记模板
docs/                      指南、架构图和案例
scripts/                   可选辅助脚本
examples/                  演示项目和资料工作流
```

部分文件名保留中文，是因为它们来自原始工作方法的内容层。英文用户可以从 `README.md`、`START-HERE.md`、`AGENTS.md`、`index.md` 和英文 docs 入口使用。

## 成熟度

当前是 `0.x` beta starter kit，适合受控试用、小范围 vault 和反馈验证；不承诺兼容所有已有 Obsidian vault 结构。

这是一套 workflow kit，不是自动化平台。如果项目状态、决策、交接和经验长期不维护，它会慢慢退化成普通文件夹。

## License

- 代码、脚本和可执行片段：[MIT](LICENSE)。
- 原创文字内容、模板、示例和文档：[CC BY 4.0](CONTENT-LICENSE.md)。
- 第三方内容不包含在本仓库授权范围内。

## Version

当前版本：`0.5.8`。见 [CHANGELOG.md](CHANGELOG.md)。
