---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- prose
- nlp
- intent
- natural-language
title: Prose 自然语言意图引擎参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/prose"
  captured_at: "2026-04-21T23:44:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Prose 自然语言意图引擎参考

**创建时间**: 2026-04-21 23:44 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Prose** 是 OpenClaw 的**自然语言意图解析引擎**，负责将用户输入的自然语言转换为结构化指令。

**核心 API**：Parse (解析)、BindSkills (绑定)、GenerateResponse (生成回复)

**Intent 结构**：Action, Entities, Params, Confidence

---

## 🔧 核心 API

### 1. 文本解析

```go
prose.Parse(input string) (Intent, error)
```

**用途**: 将自然语言转换为结构化意图

**输入**: `"请列出所有已安装技能"`

**输出**: `Intent{Action, Entities, Params, Confidence}`

---

### 2. Intent 结构体

```go
type Intent struct {
    Action     string  // 动作
    Entities   []string // 实体
    Params     map[string]interface{} // 参数
    Confidence float64  // 置信度
}
```

---

### 3. 绑定技能

```go
prose.BindSkills(skill.Registry)
```

**用途**: 关联技能系统，实现自动调用

---

### 4. 生成回复

```go
prose.GenerateResponse(ctx Intent) string
```

**用途**: 从意图生成自然语言回复

---

## 📋 使用流程

```go
// 1. 解析用户输入
intent, err := prose.Parse("请列出所有已安装技能")

// 2. 绑定技能库
prose.BindSkills(skillRegistry)

// 3. 执行并生成回复
response := prose.GenerateResponse(intent)
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 自定义意图规则 | ❌ 未提取 |
| 多轮对话上下文 | ❌ 未提取 |
| 训练语料 | ❌ 未提取 |
| 完整代码示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Skills 系统** | `skills.md` |
| **Slash Commands** | `slash-commands.md` |
| **Plugin Architecture** | `plugin-architecture.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_prose_nlp_engine_role.json`
- `../assets/genes/gene_prose_intent_structure.json`

### Capsules

- `../assets/capsules/capsule_prose_parse_text.json`
- `../assets/capsules/capsule_prose_bind_skills.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:44 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
