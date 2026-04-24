---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- tasks
- orchestration
- execution
title: Tasks 任务编排系统参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation/tasks"
  captured_at: "2026-04-21T23:48:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Tasks 任务编排系统参考

**创建时间**: 2026-04-21 23:48 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Tasks 系统**用于**任务编排与执行管理**，跟踪任务从创建到完成的整个生命周期。

**核心要素**：5 种状态、创建/查询 API、CLI 管理命令

---

## 📊 任务状态

| 状态 | 说明 |
|------|------|
| **pending** | 等待执行 |
| **running** | 正在执行 |
| **success** | 执行成功 |
| **failed** | 执行失败 |
| **cancelled** | 已取消 |

---

## 🔧 核心 API

### 创建任务

```go
task.Create(spec TaskSpec) (TaskID, error)
```

**返回**: TaskID (任务唯一标识)

---

### 查询任务

```go
task.Get(id TaskID) (TaskStatus, error)
```

**返回**: 任务状态信息

---

## 📦 CLI 命令

```bash
# 列出所有任务
openclaw task list

# 查询任务状态
openclaw task status <task-id>

# 取消任务
openclaw task cancel <task-id>
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| TaskSpec 结构 | ❌ 未提取 |
| 并发控制 | ❌ 未提取 |
| 超时与重试 | ❌ 未提取 |
| 完整示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Automation** | `automation.md` |
| **Cron Jobs** | `cron-jobs.md` |
| **Skills 系统** | `skills.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_task_state_enum.json`
- `../assets/genes/gene_task_create_api.json`

### Capsules

- `../assets/capsules/capsule_task_status_cli.json`
- `../assets/capsules/capsule_task_cancel_cli.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:48 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
