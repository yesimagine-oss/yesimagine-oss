---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- tools
- skills
- configuration
- yaml
title: 技能配置系统参考
type: article
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/skills-config"
  captured_at: "2026-04-21T23:40:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# 技能配置系统参考

**创建时间**: 2026-04-21 23:40 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 已验证

---

## 📋 执行摘要

**技能配置系统**允许通过配置文件管理技能的启用、超时、重试、认证、限流等参数。

**核心要素**：配置文件格式、5 个核心字段、加载接口、校验命令

---

## 📄 配置文件

| 项目 | 说明 |
|------|------|
| **文件名** | `skills.yaml` 或 `skills.json` |
| **格式** | YAML / JSON |
| **位置** | 项目根目录或配置目录 |

---

## 🔧 核心配置项

| 字段 | 说明 | 类型 |
|------|------|------|
| **enabled** | 是否启用 | boolean |
| **timeout** | 超时时间 | integer |
| **retries** | 重试次数 | integer |
| **auth** | 认证配置 | object |
| **rate_limit** | 限流配置 | object |

---

## 📦 加载接口

```go
skill.LoadConfig(path string) error
```

**用途**: 从文件加载技能配置

---

## 🔍 校验命令

```bash
openclaw skill config validate ./skills.yaml
```

**用途**: 检查配置文件格式与字段合法性

---

## ⚠️ 未覆盖内容

| 内容 | 状态 |
|------|------|
| 完整配置示例 | ❌ 未提取 |
| auth 字段格式 | ❌ 未提取 |
| rate_limit 规则 | ❌ 未提取 |
| 多环境配置 | ❌ 未提取 |

---

## 📚 关联文档

| 文档 | 位置 |
|------|------|
| **Skills 系统** | `skills.md` |
| **Creating Skills** | `creating-skills.md` |
| **Plugin Manifest** | `plugin-manifest.md` |

---

## 📊 资产固化

### Genes

- `../assets/genes/gene_openclaw_skill_config_file.json`
- `../assets/genes/gene_openclaw_skill_config_fields.json`

### Capsules

- `../assets/capsules/capsule_openclaw_skill_config_validate.json`

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 23:40 GMT+8  
**状态**: ✅ 已存入知识库

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
