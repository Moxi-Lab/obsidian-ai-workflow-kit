# 自动化入门

这套 kit 从 Markdown 开始，是因为规则应该可检查。自动化应该减少遗忘，而不是把重要改动藏起来。

建议从提醒和检查开始：

1. 在 AI 会话前后运行 `stale-check`。
2. 用 Claude Code Stop hook 在会话结束前提醒 Agent。
3. 让 Agent 按 `START-HERE.md` 写交接、更新项目状态和沉淀经验。

不要一开始就做静默自动改写。本地知识库更适合“人能看见变化”的自动化。

## Stale Check

```bash
python3 scripts/kb.py stale-check --vault "/path/to/your-vault"
```

它会检查：

- 项目桥接卡的 `updated` 日期是否过久；
- 项目桥接卡是否缺少 `updated` 日期；
- Inbox 里是否堆积了太多待处理文件。

如果要在 hooks 或 CI 里使用，可以让它发现问题时返回失败：

```bash
python3 scripts/kb.py stale-check \
  --vault "/path/to/your-vault" \
  --max-age-days 7 \
  --inbox-threshold 10 \
  --fail-on-findings
```

## Claude Code Hooks

Claude Code 可以通过 `.claude/settings.json` 配置项目级 hooks。本仓库的示例使用 Stop hook：当会话即将结束时，运行 `stale-check`，提醒 Agent 先检查过期项目、Inbox 堆积和是否需要写交接。

示例位置：

```text
examples/claude-code-hooks/
```

基本安装：

1. 在你的 vault 里创建 `.claude/hooks/`。
2. 把 `examples/claude-code-hooks/stop-session-check.py` 复制到 `.claude/hooks/stop-session-check.py`。
3. 把 `examples/claude-code-hooks/settings.example.json` 合并进 `.claude/settings.json`。
4. 从 vault 根目录启动 Claude Code。

这个 hook 不会编辑笔记。它只提醒本次会话是否应该写交接、更新项目桥接卡或清理 Inbox。

Claude Code hooks 官方文档：<https://docs.anthropic.com/en/docs/claude-code/hooks>

## 推荐自动化梯度

| 层级 | 自动化 | 风险 |
|---|---|---|
| 1 | 手动运行 `stale-check` | 最低 |
| 2 | Stop hook 提醒 Agent 写交接 | 低 |
| 3 | 定时 `stale-check` 写巡检报告 | 中 |
| 4 | AI 根据交接卡提出桥接卡更新建议 | 中 |
| 5 | AI 不经确认直接改桥接卡 | 高 |

公开版当前只提供第 1 层和第 2 层。更高层级应该等用户能检查和确认改动后再加入。
