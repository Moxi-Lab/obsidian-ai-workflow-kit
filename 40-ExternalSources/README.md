---
type: external-sources-readme
status: active
---

# External Sources

这里放外部资料的分析结果，不直接保存第三方原文全文。

## 处理流程

1. 本机资料先按 `02-Knowledge-Pipeline/local-material-intake.md` 判断范围和类型。
2. 外部资料先进入 `01-Inbox/web-clips/` 或用 `scripts/kb.py intake-source` 创建资料分析卡。
3. 用 `90-Templates/TPL-source-analysis-card.md` 判断资料价值。
4. 只保留摘要、来源链接、可复用点和写回去向。
5. 有长期价值的内容，写回项目、共享资产或召回地图。

## 升舱规则

- 资料分析卡留在 `40-ExternalSources/` 作为来源证据，不移动、不覆盖。
- 影响项目状态时，更新 `10-Projects/<project>/current-state.md` 或 `decisions.md`。
- 变成可复用经验时，新建问题知识卡 / 经验资产卡，或写入 `20-SharedAssets/02-modules/`。
- 需要以后被主动召回时，更新项目桥接卡或 `03-Recall-System/task-to-context-map.md`。
- 原资料分析卡默认 `canonical: false`；升舱后的权威卡才设为 `canonical: true`。

## Web Clipper 标签口径

- 原始剪藏只做路由，不直接写成问题知识卡。
- `tags` 只放来源/状态类标签，默认保留 `clippings`。
- `themes` 可先留空，分拣或提炼后再补稳定主题。
- `canonical` 原始剪藏默认 `false`，提炼后的权威问题卡或经验资产卡才设为 `true`。
- `question_text`、`applicable_to` 不写入原始剪藏，只写入 `90-Templates/TPL-question-knowledge-experience-asset-card.md`。

## 禁止项

- 不复制第三方文章全文。
- 不保存需要登录才能访问的私密内容。
- 不保存 Cookie、Token、账号信息。
