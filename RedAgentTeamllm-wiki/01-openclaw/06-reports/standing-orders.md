---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- standing-orders
- event-driven
- autonomous
title: Standing Orders 常驻指令参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation/standing-orders"
  captured_at: "2026-04-21T23:52:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Standing Orders 常驻指令参考

**创建时间**: 2026-04-21 23:52 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**Standing Orders** 是**持久化自治规则**，持续监听事件并自动执行。

**核心要素**：事件触发、Prose 条件、技能/任务动作、CLI 管理

---

## 🔍 什么是常驻指令？

**特点**：
- ✅ 持久化 (重启后还在)
- ✅ 事件驱动 (有事才动)
- ✅ 持续监听 (一直等着)
- ✅ 自动执行 (无需人工)

**比喻**：像个**保安**，一直站在那里，看到可疑人员就行动

---

## 📋 与定时任务的区别

| 特性 | Cron Jobs | Standing Orders |
|------|-----------|-----------------|
| **触发** | 时间 (每天 3 点) | 事件 (收到邮件) |
| **执行** | 到点就跑 | 有事才跑 |
| **监听** | 不监听 | 持续监听 |
| **比喻** | 闹钟 | 保安 |

---

## 🔧 核心机制

### 触发方式

```
event-based, always-listening
```

**事件示例**：
- 收到新邮件
- 有人@你
- 系统报错
- 文件变化

---

### 条件判断

```
prose.Parse + boolean expression
```

**说明**：用自然语言解析来判断是否触发

**示例**：`"邮件包含'紧急'" → 触发`

---

### 执行动作

```
skill invocation or task launch
```

**可以**：
- 调用技能
- 启动任务

---

## 📦 CLI 命令

```bash
# 列出所有常驻指令
openclaw standing list

# 启用指令
openclaw standing enable <rule-id>

# 禁用指令
openclaw standing disable <rule-id>
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 事件源类型 | ❌ 未提取 |
| 规则语法 | ❌ 未提取 |
| 持久化存储 | ❌ 未提取 |
| 完整示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Prose** | `prose.md` |
| **Tasks** | `tasks.md` |
| **Skills** | `skills.md` |
| **Automation** | `automation.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_standing_order_behavior.json`
- `../assets/genes/gene_standing_condition_prose.json`

### Capsules

- `../assets/capsules/capsule_standing_list_cli.json`
- `../assets/capsules/capsule_standing_enable_cli.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:52 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
