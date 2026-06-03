---
asset: true
asset_group: 规则资产
asset_label: 巡检清单
type: checklist
aliases: ["知识库巡检清单-v1", "Vault Health Checklist"]
updated: 2026-06-01
scope: cross-project
owner: maintainer
status: active
---

# 知识库巡检清单 v1

用于做 Obsidian 知识库的轻量健康检查，重点不是“加更多目录”，而是保证**入口可信、链接可达、状态清楚、沉淀顺畅**。

## 一、入口可信化（每周至少一次）

- [ ] `index.md` 的主入口都能打开
- [ ] `00-AI/START-HERE.md` 的开工指令和任务类型仍然准确
- [ ] `00-AI/AGENTS.md` 与 `00-AI/START-HERE.md` 的写回规则一致
- [ ] `00-AI/governance/` 的治理规则能打开
- [ ] `00-AI/pipeline/` 的资料整理流程能打开
- [ ] `00-AI/recall/` 的召回地图能打开
- [ ] `index.md` 只列出真实存在的稳定入口
- [ ] `10-Projects/` 中每个示例项目都有 README、桥接卡、当前状态和决策页
- [ ] `10-Projects/PROJECTS-REGISTRY.md` 中列出的目录与实际目录一致
- [ ] 首页、项目登记表、README 三者没有互相打架

## 二、断链与旧链接治理（每两周一次）

- [ ] 检查是否存在指向旧结构/旧命名的 wikilink
- [ ] 检查是否存在 basename 歧义链接
- [ ] 检查是否还有旧 Inbox 子目录、私有库中文目录名、旧项目代号等迁移残留
- [ ] 发现断链后，优先修“高频入口页”而不是边角文件

## 三、Inbox / 状态治理（每周一次）

- [ ] `01-Inbox/` 只承担分流，不承担长期堆积
- [ ] `01-Inbox/agent-handoffs/` 是否有长期滞留的交接卡
- [ ] `01-Inbox/web-clips/` 中的网页剪藏是否已转成资料分析卡、项目更新或共享资产
- [ ] 新增内容是否有明确状态：`draft / active / waiting / archived`
- [ ] 处理完成的内容是否有明确去向（项目、共享资产、经验资产、外部资料）

## 四、内容健康检查（每周一次）

- [ ] 检查是否存在同一主题的重复学习卡或重复剪藏
- [ ] 检查是否有旧结论被新资料推翻但未标注
- [ ] 检查是否有页面之间说法互相矛盾
- [ ] 检查是否有重要页面没有任何入站链接或关联入口
- [ ] 检查是否有反复出现的高频概念仍缺少权威页
- [ ] 检查近期高价值问答是否已回写到项目、共享资产或经验资产

## 五、项目层健康度（每两周一次）

- [ ] 每个长期项目都有桥接卡
- [ ] 项目 README 写清楚当前重点、常用入口、下一步动作
- [ ] 示例项目只保留能解释方法的最小骨架
- [ ] 项目内可复用内容是否上浮到 `20-SharedAssets/`

## 六、元数据最小标准（持续）

新增页面必须遵守 [metadata-minimum-standard-v1](./metadata-minimum-standard-v1.md)。

最小 frontmatter：

```yaml
---
type:
created:
updated:
status:
---
```

按类型再补充可选字段：

- 项目页：`owner` `stage` `priority`
- 交接卡：`source_agent` `handoff_type` `next_action`
- 外部资料：`source` `author` `captured` `related_project` `related_notes`

## 七、Agent 可调用性检查（每周一次）

- [ ] 高频任务是否能从 `00-AI/START-HERE.md` 找到下一步
- [ ] 新增规则是否已接入 `00-AI/AGENTS.md`、`00-AI/START-HERE.md`、`00-AI/governance/` 或 `20-SharedAssets/`
- [ ] 权威状态源是否少于 10 个，避免入口膨胀
- [ ] 旧交接卡、旧剪藏、旧目标是否没有覆盖当前状态页
- [ ] AI 生成内容是否经过人工确认后再写成长期规则

## 八、推荐处理优先级

1. 先修首页 / README / 项目桥接卡等高频入口
2. 再修 `00-AI/START-HERE.md`、`00-AI/AGENTS.md` 和项目桥接卡
3. 再修断链与旧链接
4. 再清 Inbox 与状态字段
5. 再查重复、矛盾、过时和孤立内容
6. 再补元数据和复用资产上浮
7. 最后才考虑继续扩目录

## 九、使用口令（可直接复制）

```text
按《知识库巡检清单 v1》执行一轮巡检：
1) 先检查 index / START-HERE / AGENTS / Agent-Governance / Knowledge-Pipeline / Recall-System / PROJECTS-REGISTRY 是否可达；
2) 列出断链、旧链接和私有库概念残留；
3) 标出 Inbox 堆积点；
4) 标出重复、矛盾、过时、孤立内容；
5) 标出空项目、弱项目；
6) 只优先修高频入口，不要一上来全库大改。
```
