---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- workflow
- cron
- orchestration
title: Automation 自动化框架参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation"
  captured_at: "2026-04-21T23:45:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Automation 自动化框架参考

**创建时间**: 2026-04-21 23:45 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Automation 框架**用于**技能编排、定时任务、事件驱动与流程自动化**。

**核心要素**：4 类触发器、工作流结构、注册 API、CLI 命令

---

## 🔧 触发器类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **schedule** | 定时调度 | 每天 9:00 执行 |
| **webhook** | HTTP 回调 | API 触发 |
| **event** | 事件驱动 | 收到邮件触发 |
| **cron** | Cron 表达式 | `0 */2 * * *` |

---

## 📦 工作流结构

```
Workflow = sequence of skills + conditionals
```

**组成**：
- 技能序列 (按顺序执行)
- 条件判断 (分支逻辑)

---

## 🔧 核心 API

### 注册工作流

```go
automation.RegisterWorkflow(name, steps)
```

| 参数 | 说明 |
|------|------|
| **name** | 工作流名称 |
| **steps** | 步骤序列 |

---

### CLI 命令

```bash
# 运行工作流
openclaw workflow run <name>
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 步骤语法 | ❌ 未提取 |
| 条件判断写法 | ❌ 未提取 |
| 异常重试策略 | ❌ 未提取 |
| YAML 配置示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Skills 系统** | `skills.md` |
| **Prose** | `prose.md` |
| **Plugin Architecture** | `plugin-architecture.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_automation_framework_purpose.json`
- `../assets/genes/gene_automation_trigger_types.json`

### Capsules

- `../assets/capsules/capsule_workflow_run_cli.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:45 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
