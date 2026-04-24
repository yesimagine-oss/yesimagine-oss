---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- tools
- slash-commands
- cli
- interaction
title: 斜杠命令框架参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/slash-commands"
  captured_at: "2026-04-21T23:41:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# 斜杠命令框架参考

**创建时间**: 2026-04-21 23:41 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Slash Commands 框架**允许自定义 `/命令` 并在交互终端中使用。

**核心 API**：Register (注册)、BindToShell (绑定)

**内置命令**：/help, /list, /reload, /status

---

## 🔧 核心 API

### 1. 注册命令

```go
slash.Register(name, usage, handler)
```

| 参数 | 说明 |
|------|------|
| **name** | 命令名称 (如 `help`) |
| **usage** | 使用说明 |
| **handler** | 处理函数 |

---

### 2. 处理函数签名

```go
func(ctx context.Context, args []string) (string, error)
```

| 参数 | 说明 |
|------|------|
| **ctx** | 上下文 |
| **args** | 命令参数数组 |
| **返回** | 输出字符串 + 错误 |

---

### 3. 绑定到 Shell

```go
slash.BindToShell()
```

**用途**: 将命令绑定到交互终端

---

## 📦 内置命令

| 命令 | 用途 |
|------|------|
| **/help** | 显示帮助 |
| **/list** | 列出命令 |
| **/reload** | 重新加载 |
| **/status** | 显示状态 |

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 完整 Go 示例代码 | ❌ 未提取 |
| 参数解析规则 | ❌ 未提取 |
| 权限控制 | ❌ 未提取 |
| 自动补全机制 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Skills 系统** | `skills.md` |
| **SDK Runtime** | `sdk-runtime.md` |
| **SDK Agent Harness** | `sdk-agent-harness.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_openclaw_slash_handler_signature.json`
- `../assets/genes/gene_openclaw_slash_builtin.json`

### Capsules

- `../assets/capsules/capsule_openclaw_slash_shell_bind.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:41 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
