---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- cron
- scheduling
-定时任务
title: Cron Jobs 定时任务参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation/cron-jobs"
  captured_at: "2026-04-21T23:47:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Cron Jobs 定时任务参考

**创建时间**: 2026-04-21 23:47 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Cron Jobs** 是 OpenClaw 的**定时任务调度系统**，用于按 cron 表达式自动执行技能。

**核心要素**：5 位 cron 语法、创建接口、CLI 管理命令

---

## 🔧 Cron 表达式语法

**标准 5 位格式**：
```
分 时 日 月 周
```

**示例**：
| 表达式 | 含义 |
|--------|------|
| `0 3 * * *` | 每天 3:00 执行 |
| `*/5 * * * *` | 每 5 分钟执行 |
| `0 9 * * 1` | 每周一 9:00 执行 |
| `0 0 1 * *` | 每月 1 号 0:00 执行 |

---

## 🔧 核心 API

### 创建任务

```go
cron.Create(name, expr, skillID)
```

| 参数 | 说明 |
|------|------|
| **name** | 任务名称 |
| **expr** | cron 表达式 |
| **skillID** | 要执行的技能 |

---

### 列出任务

```go
cron.List() []CronJob
```

**返回**: 所有定时任务列表

---

## 📦 CLI 命令

```bash
# 列出所有任务
openclaw cron list

# 添加任务
openclaw cron add "daily-check" "0 3 * * *" skill-backup

# 删除任务
openclaw cron delete <name>
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 时区配置 | ❌ 未提取 |
| 失败重试 | ❌ 未提取 |
| 任务日志 | ❌ 未提取 |
| 完整示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Automation** | `automation.md` |
| **Skills 系统** | `skills.md` |
| **Plugin Architecture** | `plugin-architecture.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_cron_standard_syntax.json`
- `../assets/genes/gene_cron_create_api.json`

### Capsules

- `../assets/capsules/capsule_cron_list_cli.json`
- `../assets/capsules/capsule_cron_add_cli.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:47 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
