# 30 秒演示

如果你还不想安装到自己的 vault，可以先用这个方式看懂效果。

## 步骤

1. 下载或克隆这个仓库。
2. 打开 Obsidian，选择 **Open folder as vault**，选中这个仓库目录。vault 本质上就是一个本地 Markdown 文件夹。
3. 把这段话发给一个能读取本地文件的 AI Agent：

```text
你是知识库维护 Agent。这个 Obsidian vault 的根目录是：<这个仓库的本地路径>。请先读取 00-AI/START-HERE.md，然后使用 examples/filled-example 里的只读演示项目。告诉我当前项目状态、最新决策和下一步动作。不要编辑文件或创建任务卡。
```

## 预期效果

AI 应该读取：

- `00-AI/START-HERE.md`
- `index.md`
- `examples/filled-example/BRIDGE-launch-notes.md`
- `examples/filled-example/current-state.md`
- `examples/filled-example/decisions.md`

然后说明演示项目的当前状态、最新决策、下一步动作，以及真实任务应该写回哪里。
