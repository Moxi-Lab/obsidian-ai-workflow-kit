# Before / After 案例

这个案例说明这套结构如何处理一个小型混乱资料夹。它不是全自动承诺。用户仍然要判断什么重要，AI 也必须先读规则，再写回正确位置。

## 整理前

```text
~/Downloads/product-launch/
├── call-notes.txt
├── competitor-links.md
├── draft-positioning.md
├── onboarding-research.pdf
├── random-screenshot.png
└── todo-from-chat.md
```

这些资料有价值，但新的 AI 会话不知道：

- 属于哪个项目
- 哪个文件是当前状态
- 哪些是资料、决策或任务
- 摘要应该写到哪里
- 下次应该从哪里召回

## 第一次进入

用户先生成目录清单，而不是让 AI 直接读完整资料夹：

```bash
python3 00-AI/scripts/kb.py intake-folder ~/Downloads/product-launch \
  --title "Product Launch Materials" \
  --project product-launch
```

这会生成：

```text
40-ExternalSources/02-folder-intakes/product-launch-materials.md
```

这张导入卡只列出文件，不移动原文件，并提醒 AI 先处理一小部分，再决定是否升舱。

## AI 分流

AI 读完 `00-AI/START-HERE.md` 后，应该这样分流：

| 输入 | 知识类型 | 写回位置 |
|---|---|---|
| `call-notes.txt` | 项目状态 | `10-Projects/product-launch/current-state.md` |
| `draft-positioning.md` | 候选决策 | `10-Projects/product-launch/decisions.md` |
| `onboarding-research.pdf` | 资料证据 | `40-ExternalSources/01-samples/` |
| `todo-from-chat.md` | 临时任务记录 | 项目桥接卡下一步或 Inbox |
| 过程中反复出现的经验 | 可复用资产 | `20-SharedAssets/02-modules/` |

## 整理后

```text
10-Projects/product-launch/
├── BRIDGE-product-launch.md
├── current-state.md
└── decisions.md

40-ExternalSources/
├── 01-samples/onboarding-research.md
└── 02-folder-intakes/product-launch-materials.md

00-AI/recall/task-to-context-map.md
20-SharedAssets/02-modules/<reusable-lesson>.md
```

之后新的 AI 会话可以从项目桥接卡开始，只读任务需要的上下文，并把结果写回正确位置。

## 这套结构不会做什么

- 不替你决定项目策略。
- 不扫描整台电脑。
- 如果没有人持续更新项目状态、决策、交接和经验，它不会自动保持有用。
- 不替代 Obsidian，只是给 Obsidian 加一套 AI 能执行的工作流。
