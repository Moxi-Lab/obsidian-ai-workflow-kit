---
type: governance-rule
status: active
---

# Startup Contract

AI 每次开工先读 `00-AI/START-HERE.md`，再按任务类型读取最少上下文。

当前对话能完成的任务直接执行，不先创建任务卡或认领岗位角色。只有排队、跨会话、阻塞或明确协调的工作才进入 `01-Inbox/tasks/`。

## 回执格式

```text
已读取 00-AI/START-HERE.md
任务类型：<整理本机资料 / 接手项目 / 整理外部资料 / 沉淀经验 / 维护知识库 / 写交接 / 待确认>
下一步先读：<具体文件>
结果写回：<具体目录或文件>
不会做：<本轮明确不做的事>
```

## 上下文预算

| 任务 | 首轮最多读取 |
|---|---|
| 整理本机资料 | `00-AI/START-HERE.md`、`00-AI/pipeline/README.md`、`00-AI/pipeline/local-material-intake.md` |
| 接手项目 | `00-AI/START-HERE.md`、项目桥接卡、`current-state.md`、`decisions.md` |
| 资料整理 | `40-ExternalSources/README.md`、资料分析模板 |
| 经验沉淀 | 经验资产化机制、问题知识卡模板 |
| 维护知识库 | 巡检清单、召回地图、健康检查结果 |
| 接续本地任务 | 对应任务卡、项目桥接卡、验收证据 |

## 禁止行为

- 不在没有任务目标时全库扫描。
- 不把 Inbox 当长期存储。
- 不把私人凭据、账号信息、Token、Cookie 写入 vault。
- 不用没有来源的推测覆盖已有事实。
- 不默认创建 CEO、CTO、QA 等岗位角色卡；需要专业视角时直接写明检查角度。
