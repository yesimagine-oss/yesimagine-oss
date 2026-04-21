---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- sdk
- plugin
- manifest
- configuration
title: 插件清单文件规范
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/manifest"
  captured_at: "2026-04-21T23:35:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# 插件清单文件规范

**创建时间**: 2026-04-21 23:35 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**插件清单 (plugin.yaml)** 是每个 OpenClaw 插件的**身份证**。

**5 个核心要素**：文件名、6 个必填字段、6 类插件类型、校验命令

---

## 📄 清单文件

| 项目 | 要求 |
|------|------|
| **文件名** | `plugin.yaml` |
| **位置** | 插件根目录 |
| **必填** | ✅ 是 |
| **格式** | YAML |

---

## 🔧 必填字段

| 字段 | 说明 | 示例 |
|------|------|------|
| **id** | 插件唯一标识 | `my-plugin` |
| **name** | 插件显示名称 | `My Plugin` |
| **version** | 版本号 | `1.0.0` |
| **author** | 作者 | `Your Name` |
| **type** | 插件类型 | `provider` |
| **sdk_version** | SDK 版本 | `1.0.0` |

---

## 📦 插件类型

| 类型 | 用途 |
|------|------|
| **provider** | 模型提供商 |
| **channel** | 通信渠道 (微信/Telegram 等) |
| **memory** | 记忆存储 |
| **auth** | 认证授权 |
| **ui** | 用户界面 |
| **harness** | 编排调度 |

---

## 📋 最小示例

```yaml
id: my-plugin
name: My Plugin
version: 1.0.0
author: Your Name
type: provider
sdk_version: 1.0.0
```

---

## 🔍 校验命令

```bash
# 校验清单格式
openclaw plugin lint manifest
```

**验证**：
- 字段完整性
- 格式合法性
- 类型有效性

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 字段格式约束 | ❌ 未提取 |
| 版本号语义化规则 | ❌ 未提取 |
| 插件依赖声明 | ❌ 未提取 |
| 完整示例 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **SDK Setup** | `sdk-setup.md` |
| **SDK Testing** | `sdk-testing.md` |
| **SDK Entrypoints** | `sdk-entrypoints.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_openclaw_plugin_manifest_file.json`
- `../assets/genes/gene_openclaw_plugin_manifest_fields.json`

### Capsules

- `../assets/capsules/capsule_openclaw_manifest_validate.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:35 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
