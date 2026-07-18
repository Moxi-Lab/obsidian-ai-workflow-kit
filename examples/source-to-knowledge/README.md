---
type: example
status: active
---

# Source To Knowledge Example

这个示例展示一份本机资料如何进入知识库，并最终变成可召回知识。

## 场景

用户给 AI 一个本地文件：

```text
<source-file-path>/onboarding-research.md
```

用户说：

```text
请把这份资料整理进我的 Obsidian 知识库。
```

## AI 应该怎么做

1. 先读 `00-AI/START-HERE.md`。
2. 判断任务类型是“整理本机资料”。
3. 读取 `00-AI/pipeline/local-material-intake.md`。
4. 先创建资料分析卡，不直接复制全文。
5. 判断是否影响项目、经验资产或召回地图。

## 示例产物

- `source-analysis-onboarding-research.md`
- `promoted-question-card.md`
