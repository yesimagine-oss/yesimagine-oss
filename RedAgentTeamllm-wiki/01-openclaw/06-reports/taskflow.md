---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- taskflow
- workflow
- dag
title: TaskFlow 工作流引擎参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation/taskflow"
  captured_at: "2026-04-21T23:50:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# TaskFlow 工作流引擎参考

**创建时间**: 2026-04-21 23:50 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**TaskFlow** 是 OpenClaw 的**工作流编排引擎**，基于**DAG（有向无环图）**组织多个任务的执行顺序。

**核心要素**：DAG 结构、定义接口、启动/控制 CLI

---

## 🔄 什么是 DAG？

**DAG** = Directed Acyclic Graph = 有向无环图

**简单说**：任务之间有依赖关系，不能循环

**示例**：
```
任务 A → 任务 B → 任务 C
         ↓
       任务 D
```
- B 和 C 必须等 A 完成
- D 必须等 B 完成
- 不能 A→B→A（不能循环）

---

## 🔧 核心 API

### 定义工作流

```go
taskflow.Define(name string, dag DAG)
```

| 参数 | 说明 |
|------|------|
| **name** | 工作流名称 |
| **dag** | DAG 结构定义 |

---

### 启动工作流

```go
taskflow.Start(flowID string) (RunID, error)
```

**返回**: RunID (运行实例 ID)

---

## 📦 CLI 命令

```bash
# 运行工作流
openclaw taskflow run <flow-name>

# 查看状态
openclaw taskflow status <run-id>

# 暂停工作流
openclaw taskflow pause <run-id>
```

---

## 🆚 与 Cron Jobs 的区别

| 特性 | Cron Jobs | TaskFlow |
|------|-----------|----------|
| **用途** | 定时触发 | 任务编排 |
| **触发方式** | 时间 (cron 表达式) | 手动/API/事件 |
| **任务关系** | 独立执行 | 有依赖关系 |
| **示例** | 每天 3:00 备份 | 备份→压缩→上传 |

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| DAG 语法 | ❌ 未提取 |
| 数据传递 | ❌ 未提取 |
| 条件分支 | ❌ 未提取 |
| 完整示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Tasks** | `tasks.md` |
| **Cron Jobs** | `cron-jobs.md` |
| **Automation** | `automation.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_taskflow_dag_based.json`
- `../assets/genes/gene_taskflow_define_api.json`

### Capsules

- `../assets/capsules/capsule_taskflow_run_cli.json`
- `../assets/capsules/capsule_taskflow_status_cli.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:50 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
