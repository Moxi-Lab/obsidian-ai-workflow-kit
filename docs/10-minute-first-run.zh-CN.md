# 10 分钟首次体验

这条路径适合新用户快速看到价值，不需要重建自己的完整 vault。

新建 Vault 时，直接用 managed installer 安装到空目录；需要完整 starter 结构时再加 `--mode full`。下面先用更小的默认模式验证工作流，再决定是否扩展。

## 0. 先用测试 vault

先用空目录或一个很小的测试 vault。不要一开始就拿完整个人 vault 测试。

```bash
mkdir -p ~/obsidian-ai-workflow-test
mkdir -p ~/demo-materials
printf "示例资料。\n" > ~/demo-materials/example.md
```

## 1. 预览安装

如果仓库已经 public：

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN --dry-run ~/obsidian-ai-workflow-test
```

如果你已经克隆仓库：

```bash
bash install.sh --language zh-CN --dry-run ~/obsidian-ai-workflow-test
```

## 2. 安装

如果仓库已经 public：

```bash
curl -fsSL https://raw.githubusercontent.com/HiHeiBai/obsidian-ai-workflow-kit/main/install.sh | bash -s -- --language zh-CN ~/obsidian-ai-workflow-test
```

如果你已经克隆仓库：

```bash
bash install.sh --language zh-CN ~/obsidian-ai-workflow-test
```

安装脚本默认跳过已有文件。

## 3. 验证

```bash
python3 ~/obsidian-ai-workflow-test/90-系统/脚本/kb.py health-check --vault ~/obsidian-ai-workflow-test --mode barebone
```

## 4. 创建项目桥接卡

```bash
python3 ~/obsidian-ai-workflow-test/90-系统/脚本/kb.py new-project demo-project \
  --vault ~/obsidian-ai-workflow-test \
  --name "Demo Project" \
  --root ~/demo-project
```

## 5. 创建资料目录清单

把它指向一个只有少量文件的测试资料夹：

```bash
python3 ~/obsidian-ai-workflow-test/90-系统/脚本/kb.py intake-folder ~/demo-materials \
  --vault ~/obsidian-ai-workflow-test \
  --title "Demo Materials" \
  --project demo-project
```

这一步只生成清单，不移动、不改写原文件。

## 6. 让 AI 开工

把这句话发给能读取本地文件的 AI 工具：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：~/obsidian-ai-workflow-test。请先读取该目录下的 00-入口/开始这里.md，并按里面的开工流程执行。
```

预期第一条回复应包含：

```text
已读取 00-入口/开始这里.md
任务类型：<...>
下一步先读：<...>
结果写回：<...>
不会做：<...>
```

## 7. 运行 vault 审计

```bash
python3 ~/obsidian-ai-workflow-test/90-系统/脚本/kb.py audit-vault \
  --vault ~/obsidian-ai-workflow-test \
  --write-report
```

报告会写入：

```text
30-经验资产/05-audit-reports/
```

## 成功标准

你现在应该得到：

- 一个 AI 开工入口。
- 一张项目桥接卡。
- 一张资料目录导入清单。
- 一份审计报告。
- 一句可以直接发给 AI 的开工指令。
- 一个设置了 `project_entry: true`、能进入 full 模式项目 Base 的项目桥接卡。
- 当前对话能完成的任务直接执行，不额外创建本地任务卡。
