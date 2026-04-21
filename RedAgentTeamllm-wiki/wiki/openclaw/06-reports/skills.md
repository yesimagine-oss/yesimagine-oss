---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- tools
- skills
- registration
- invocation
title: Skills 技能系统参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/skills"
  captured_at: "2026-04-21T23:37:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Skills 技能系统参考

**创建时间**: 2026-04-21 23:37 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Skills 技能系统**允许插件将能力注册为智能体可调用的工具。

**核心 API**：Register (注册)、Invoke (调用)、List (列举)

**校验机制**：JSON Schema 输入/输出验证

---

## 🔧 核心 API

### 1. 注册技能

```go
skill.Register(name, handler, schema)
```

| 参数 | 说明 |
|------|------|
| **name** | 技能唯一名称 |
| **handler** | 处理函数 |
| **schema** | JSON Schema 校验规则 |

---

### 2. 调用技能

```go
skill.Invoke(ctx, name, params) error
```

| 参数 | 说明 |
|------|------|
| **ctx** | 上下文 |
| **name** | 技能名称 |
| **params** | 参数 (JSON) |

---

### 3. 列出技能

```go
skill.List() []SkillInfo
```

**返回**: 已注册技能列表

---

## 📋 校验机制

| 特性 | 说明 |
|------|------|
| **方式** | JSON Schema |
| **范围** | 输入 + 输出 |
| **目的** | 类型安全、参数验证 |

---

## 📦 CLI 命令

```bash
# 列出已注册技能
openclaw skill list

# 调用技能
openclaw skill invoke 'skill-name' '{}'
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| SkillInfo 结构体定义 | ❌ 未提取 |
| JSON Schema 示例模板 | ❌ 未提取 |
| 调用权限控制 | ❌ 未提取 |
| 技能热重载 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **SDK Entrypoints** | `sdk-entrypoints.md` |
| **SDK Agent Harness** | `sdk-agent-harness.md` |
| **Plugin Architecture** | `plugin-architecture.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_openclaw_skill_register_api.json`
- `../assets/genes/gene_openclaw_skill_validation.json`

### Capsules

- `../assets/capsules/capsule_openclaw_skill_list.json`
- `../assets/capsules/capsule_openclaw_skill_invoke.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:37 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
