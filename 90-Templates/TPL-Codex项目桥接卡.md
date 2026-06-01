---
type: template
created: 2026-05-14
updated: 2026-05-24
status: active
---

# TPL｜Codex 项目桥接卡

```yaml
---
type: codex-project-bridge
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active # active / waiting / paused / archived
pillar:
project:
local_root:
kb_project:
context_pack:
owner:
kb_bridge_status: kb-only # kb-only / project-linked / paused
last_verified:
---
```

# Codex 项目桥接卡｜<项目名>

## 一句话定位

这个本地 Codex 项目对应知识库中的哪条业务主线，以及当前为什么需要接入。

## 本地项目

| 项目 | 内容 |
|---|---|
| 本地路径 | `<local_root>` |
| Git 状态 | `<clean / dirty / unknown>` |
| 项目规则 | `AGENTS.md` |
| KB Bridge | `<已加入 / 待加入 / 不适用>` |
| 关键文档 | `docs/...` |

## 知识库映射

| 项目 | 内容 |
|---|---|
| 主线 | `<pillar>` |
| 知识库项目页 | `<Obsidian 链接>` |
| Context Pack | `<Obsidian 链接>` |
| 交接卡位置 | `01-收件箱Inbox/Agent交接卡/` |

## 开工必读

1. 项目根 `AGENTS.md`
2. 对应 context pack
3. 知识库项目页
4. 项目 docs 中的当前任务文档

## 项目记忆槽

写入原则：只写长期有效、之后会反复用到的信息；不保存完整聊天记录、流水账和敏感信息。事实和推断分开，旧信息过时时先标注“已过时”并说明原因。

### 当前状态

- `<YYYY-MM-DD｜来源任务｜项目现在处于什么状态，有什么已知限制>`

### 最近决策

- `<YYYY-MM-DD｜来源任务｜最近一次稳定决策，以及为什么这么定>`

### 下次开工

- `<YYYY-MM-DD｜来源任务｜下次 Codex 进入项目后第一件该做的事>`

### 可沉淀经验

- `<YYYY-MM-DD｜来源任务｜可复用经验 / 暂不沉淀及原因>`

## 写回规则

- 项目状态变化：更新知识库项目页和本桥接卡。
- 重要实现 / 验收：更新项目 docs，并在交接卡摘要。
- 可复用经验：上浮到共享资产或经验库。
- 重要、持续或跨项目任务结束时，至少检查本卡“当前状态 / 最近决策 / 下次开工 / 可沉淀经验”四项；有变化才更新。
- 未闭环事项写入交接卡或项目页，不散落在聊天里。

## 项目 AGENTS.md 最小入口

```md
## KB Bridge

- 知识库入口：<你的知识库路径>/START-HERE.md
- 项目登记：<你的知识库路径>/<项目登记文件>.md
- 项目桥接卡：<本卡路径>
- 项目状态变化后，更新项目桥接卡或知识库交接卡。
```

## 当前下一步

- [ ] `<下一步动作>`

## 验证记录

- `<YYYY-MM-DD>`：`<验证内容>`
