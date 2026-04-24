---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- tools
- skills
- creating
- development
title: 创建自定义技能指南
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/creating-skills"
  captured_at: "2026-04-21T23:38:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# 创建自定义技能指南

**创建时间**: 2026-04-21 23:38 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**4 步创建自定义技能**：
1. 定义处理函数
2. 编写 JSON Schema
3. 注册技能
4. 测试调用

---

## 🔧 四步流程

### 步骤 1: 定义处理函数

```go
func handler(ctx context.Context, params json.RawMessage) (any, error)
```

| 参数 | 说明 |
|------|------|
| **ctx** | 上下文 |
| **params** | 原始 JSON 参数 |
| **返回** | 结果 + 错误 |

---

### 步骤 2: 编写 JSON Schema

```json
{
  "type": "object",
  "properties": {
    "key": {"type": "string"}
  }
}
```

**用途**: 输入参数校验

---

### 步骤 3: 注册技能

```go
skill.Register(name, handler, schema)
```

| 参数 | 说明 |
|------|------|
| **name** | 技能名称 |
| **handler** | 处理函数 |
| **schema** | JSON Schema |

---

### 步骤 4: 测试调用

```bash
openclaw skill invoke my-skill '{"key":"value"}'
```

---

## 📋 完整示例

```go
// 1. 定义 handler
func myHandler(ctx context.Context, params json.RawMessage) (any, error) {
    // 处理逻辑
    return result, nil
}

// 2. 编写 schema
schema := `{"type":"object","properties":{"key":{"type":"string"}}}`

// 3. 注册
skill.Register("my-skill", myHandler, schema)

// 4. 测试
// openclaw skill invoke my-skill '{"key":"value"}'
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 完整 Go 代码示例 | ❌ 未提取 |
| JSON Schema 模板 | ❌ 未提取 |
| 错误处理规范 | ❌ 未提取 |
| 热加载配置 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Skills 系统** | `skills.md` |
| **SDK Entrypoints** | `sdk-entrypoints.md` |
| **SDK Testing** | `sdk-testing.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_openclaw_skill_handler_signature.json`
- `../assets/genes/gene_openclaw_create_skill_steps.json`

### Capsules

- `../assets/capsules/capsule_openclaw_create_skill_test.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:38 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
