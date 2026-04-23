---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- sdk
- agent-harness
- plugins
- orchestration
title: SDK Agent Harness 核心 API 参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/sdk-agent-harness"
  captured_at: "2026-04-21T23:25:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# SDK Agent Harness 核心 API 参考

**创建时间**: 2026-04-21 23:25 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Agent Harness** 是 OpenClaw SDK 中用于**编排多插件智能体工作流**的核心框架。

**标准流程**: `NewHarness()` → `Register()` → `Start()`

---

## 🎯 核心用途

| 功能 | 说明 |
|------|------|
| **多插件编排** | 统一调度多个插件构成完整智能体 |
| **生命周期管理** | 管理插件的注册、启动、停止 |
| **上下文传递** | 在插件间传递执行上下文 |
| **错误处理** | 统一的异常捕获与恢复机制 |

---

## 🔧 核心 API

### 1. 创建 Harness

```go
func NewHarness() *Harness
```

**用途**: 创建 Harness 实例

**示例**:
```go
harness := NewHarness()
```

---

### 2. 注册插件

```go
func (h *Harness) Register(p plugin.Plugin) error
```

**用途**: 将插件注册到调度器

**示例**:
```go
err := harness.Register(myPlugin)
if err != nil {
    log.Fatal(err)
}
```

---

### 3. 启动调度

```go
func (h *Harness) Start(ctx context.Context) error
```

**用途**: 启动整个智能体调度系统

**示例**:
```go
ctx := context.Background()
err := harness.Start(ctx)
if err != nil {
    log.Fatal(err)
}
```

---

## 📋 标准启动流程

```go
// 1. 创建 Harness
harness := NewHarness()

// 2. 注册插件
harness.Register(plugin1)
harness.Register(plugin2)

// 3. 启动调度
ctx := context.Background()
harness.Start(ctx)
```

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **SDK Entrypoints** | `sdk-entrypoints.md` |
| **SDK Runtime** | `sdk-runtime.md` |
| **SDK Overview** | `sdk-overview.md` |

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| Harness 配置结构 | ❌ 未提取 |
| 并发策略 | ❌ 未提取 |
| 插件间通信规范 | ❌ 未提取 |
| 故障恢复机制 | ❌ 未提取 |
| 完整编排示例 | ❌ 未提取 |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_openclaw_sdk_agent_harness_purpose.json`
- `../assets/genes/gene_openclaw_sdk_harness_core_methods.json`

### Capsules

- `../assets/capsules/capsule_openclaw_harness_register_plugin.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:25 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
