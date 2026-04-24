---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- clawhub
- registry
- plugins
- skills
title: ClawHub 插件仓库参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/clawhub"
  captured_at: "2026-04-21T23:43:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# ClawHub 插件仓库参考

**创建时间**: 2026-04-21 23:43 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**ClawHub** 是 OpenClaw 的**插件与技能中心化注册与分发仓库**。

**核心 CLI**：login、publish、search、install

---

## 🔧 核心命令

| 命令 | 用途 | 示例 |
|------|------|------|
| **login** | 登录账号 | `clawhub login --token=xxx` |
| **publish** | 发布插件 | `clawhub publish ./plugin.so` |
| **search** | 搜索插件 | `clawhub search <query>` |
| **install** | 安装插件 | `clawhub install <plugin-id>` |

---

## 📦 使用流程

```bash
# 1. 登录
clawhub login --token=your-token

# 2. 搜索插件
clawhub search my-plugin

# 3. 安装插件
clawhub install my-plugin

# 4. 发布插件 (开发者)
clawhub publish ./plugin.so
```

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 版本管理 | ❌ 未提取 |
| 私有仓库配置 | ❌ 未提取 |
| 权限控制 | ❌ 未提取 |
| 更新/删除命令 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Plugin Manifest** | `plugin-manifest.md` |
| **Skills 系统** | `skills.md` |
| **SDK Testing** | `sdk-testing.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_clawhub_registry_role.json`
- `../assets/genes/gene_clawhub_core_cli_commands.json`

### Capsules

- `../assets/capsules/capsule_clawhub_plugin_publish.json`
- `../assets/capsules/capsule_clawhub_plugin_install.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:43 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
