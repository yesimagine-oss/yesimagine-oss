---
category: yaml
created_at: '2026-04-22'
tags:
- yaml
- serialization
- syntax
- verified
title: YAML 官方基础语法
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://yaml.org"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "curl+grep"
  trust_score: 1.0

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# YAML 官方基础语法

**来源**: https://yaml.org  
**验证时间**: 2026-04-22  
**状态**: 🟡 仅主页面，待补充规范/速查卡/FAQ

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| 采样页面 | 1/5+ (仅首页) |
| 已验证事实 | 5 |
| 候选事实 | 3 |
| 可信度 | 0.99-1.0 |
| 证据等级 | 原文 + 实测 |

---

## 🎯 核心定义

| 定义 | 原文 |
|------|------|
| **全称** | YAML Ain't Markup Language™ |
| **定位** | Human Friendly Data Serialization Standard |
| **类型** | 数据序列化标准 |

---

## 📝 基础语法

### 1. 键值对

```yaml
key: value
```

**规则**: 冒号后必须有空格

---

### 2. 列表

```yaml
- item1
- item2
```

**规则**: 以 `-` 开头

---

### 3. 注释

```yaml
# This is a comment
```

**规则**: 以 `#` 开头

---

## ✅ 已验证事实清单

| 事实 | 验证命令 | 可信度 |
|------|---------|--------|
| YAML 全称 | `curl -s yaml.org \| grep "YAML Ain't"` | 1.0 |
| YAML 定位 | `curl -s yaml.org \| grep "Human Friendly"` | 1.0 |
| 键值语法 | `curl -s yaml.org \| grep "key:"` | 1.0 |
| 列表语法 | `curl -s yaml.org \| grep "^\s*-"` | 1.0 |
| 注释语法 | `curl -s yaml.org \| grep "^#"` | 1.0 |

---

## 🟡 待验证内容

| 内容 | 原因 | 建议来源 |
|------|------|---------|
| 完整规范版本 | 首页未显示 | yaml.org/spec/ |
| 嵌套对象语法 | 首页未展示 | yaml.org/refcard.html |
| 数据类型 | 首页未展示 | yaml.org/faq.html |

---

## 📦 关联资产

| 资产类型 | 资产 ID | 状态 |
|---------|--------|------|
| Gene | `gene_yaml_full_name` | ✅ 待固化 |
| Gene | `gene_yaml_basic_syntax` | ✅ 待固化 |
| Capsule | `capsule_yaml_validate_basic` | ✅ 待固化 |

---

**覆盖结论**: 仅覆盖首页基础信息，不可用于生产级配置编写  
**下一步**: 抓取 spec/refcard/faq 子页面
