---
asset: true
asset_group: 规则资产
asset_label: AI知识库复利维护SOP
type: sop
created: 2026-04-12
updated: 2026-06-01
scope: cross-project
owner: maintainer
status: active
source_note: "Public adaptation. Source materials are not included in this repository."
tags:
  - knowledge-base
  - llm-wiki
  - obsidian
  - maintenance
---

# AI 知识库复利维护 SOP v1

用于把外部资料、对话结论和项目经验转成长期可复用知识。重点不是增加目录，而是让已有结构持续生长。

## 一、适用场景

- 用户让 Agent 看文章、学习资料、分析链接。
- 一次对话产生了稳定判断、方法、清单或复盘。
- 项目中出现了可复用经验。
- 定期巡检知识库健康状况。

## 二、四步闭环

### 1. 导入

外部资料先进 `01-Inbox/web-clips/`，或直接进入 `40-ExternalSources/` 的资料分析卡。

导入时必须判断：

- 归属哪个项目或主题。
- 是否影响当前项目。
- 是否有可执行动作。
- 是否值得上浮为共享资产或经验资产。

### 2. 串联

整理学习卡时至少补齐：

- `one_liner`
- `key_insight`
- `related_project`
- `related_notes`
- `themes`

如果已有相近资料，优先合并或互链，不重复新建同类页面。

### 3. 回写

当资料或问答产生稳定结论时，按价值回写：

| 结论类型 | 回写位置 |
|---|---|
| 只用于理解来源 | `40-ExternalSources/` |
| 影响某个项目动作 | `10-Projects/<project>/` |
| 多个项目可复用 | `20-SharedAssets/` |
| 反复踩坑或稳定经验 | `90-Templates/TPL-问题知识卡-经验资产卡.md` 或 `20-SharedAssets/02-modules/` |
| 旧项目经验需要被 AI 复用 | [Codex项目经验资产化机制-v1](./Codex项目经验资产化机制-v1.md) + 对应项目桥接卡 |
| 影响当前优先级 | 对应项目桥接卡或 `10-Projects/README.md` |

没有回写去向的学习卡，只算收录，不算完成吸收。

### 4. 巡检

每周做一次轻量检查：

- Inbox 是否堆积。
- 学习卡是否缺少关联去向。
- 是否存在同主题重复资料。
- 是否有旧结论被新资料推翻。
- 是否有高频概念缺少权威页。
- 是否有好答案停留在聊天中，没有写回知识库。
- 是否有“复用=是”的经验只停留在 INBOX，没有进入经验资产或项目桥接卡。

## 三、禁止项

- 不新增 `raw/`、`wiki/`、`log.md` 等重复目录。
- 不为了单篇文章新增一套规则。
- 不把普通文章观点直接写入 Agent-OS。
- 不把每篇资料拆成大量概念页。
- 不在没有用户确认时做结构性迁移。

## 四、使用口令

```text
按《AI知识库复利维护SOP v1》处理这条输入：
1) 判断它属于哪个项目或主题；
2) 提炼 one_liner 和 key_insight；
3) 标出 related_project / related_notes / themes；
4) 判断是否需要回写到项目、共享资产或经验资产；
5) 只做必要沉淀，不新增重复目录。
```

## 五、验收标准

- 原文或来源可追溯。
- 学习卡能从 README、项目桥接卡或资料索引找到。
- 有明确回写去向，或明确标注“仅参考”。
- 可复用内容已上浮到共享资产或经验资产。
- 处理后的原始剪藏不继续滞留在 Inbox。
