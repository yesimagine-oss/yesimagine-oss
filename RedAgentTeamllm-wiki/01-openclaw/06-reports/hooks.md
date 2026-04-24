---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- hooks
- events
- callbacks
title: Hooks 事件钩子参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation/hooks"
  captured_at: "2026-04-21T23:55:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Hooks 事件钩子参考

**创建时间**: 2026-04-21 23:55 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Hooks** 是**系统与插件事件钩子**，用于在特定事件发生时自动执行回调函数。

**核心要素**：内置事件、注册接口、载荷数据、CLI 管理

---

## 🔔 内置事件

| 事件 | 触发时机 |
|------|----------|
| **task_start** | 任务开始执行 |
| **task_fail** | 任务执行失败 |
| **workflow_complete** | 工作流完成 |
| **plugin_load** | 插件加载 |

---

## 🔧 核心 API

### 注册钩子

```go
hook.On(event string, handler HookHandler)
```

| 参数 | 说明 |
|------|------|
| **event** | 事件名称 |
| **handler** | 处理函数 |

---

### 事件载荷

```go
Payload: map[string]interface{}
```

**包含**: 上下文数据 (任务 ID、错误信息、时间戳等)

---

## 📦 CLI 命令

```bash
# 列出所有钩子
openclaw hook list

# 手动触发事件
openclaw hook trigger task_fail --payload '{}'

# 测试钩子
openclaw hook test <hook-id>
```

---

## 💡 使用示例

```go
// 任务失败时发送通知
hook.On("task_fail", func(payload map[string]interface{}) {
    sendNotification("任务失败：" + payload["task_id"])
})

// 工作流完成时清理
hook.On("workflow_complete", func(payload map[string]interface{}) {
    cleanupTempFiles()
})
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 异步/同步执行 | ❌ 未提取 |
| 超时与重试 | ❌ 未提取 |
| 自定义事件 | ❌ 未提取 |
| 完整示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Tasks** | `tasks.md` |
| **TaskFlow** | `taskflow.md` |
| **Plugin Manifest** | `plugin-manifest.md` |
| **Automation** | `automation.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_hook_builtin_events.json`
- `../assets/genes/gene_hook_register_api.json`

### Capsules

- `../assets/capsules/capsule_hook_list_cli.json`
- `../assets/capsules/capsule_hook_trigger_cli.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:55 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
