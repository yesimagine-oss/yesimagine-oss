---
category: openclaw
created_at: '2026-04-22'
tags:
- hubs
- start
- verified
title: Hubs 入门指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/start/hubs"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Hubs 入门指南

**来源**: https://docs.openclaw.ai/start/hubs  
**验证时间**: 2026-04-22 01:15 GMT+8  
**状态**: 🟡 仅主页面，待补充创建流程与配置格式

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ OpenClaw Hubs Getting Started |
| **配置目录** | ✅ /var/lib/openclaw/hubs |
| **启动命令** | ✅ openclaw hub start |
| **列表命令** | ✅ openclaw hub list |
| **停止命令** | ✅ openclaw hub stop |
| **创建流程** | ❌ 缺详细步骤 |
| **配置格式** | ❌ 缺示例 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_hubs_start_title` | 入门文档标题 | `grep "OpenClaw Hubs Getting Started"` |
| `gene_openclaw_hub_config_dir` | 配置目录 | `grep "/var/lib/openclaw/hubs"` |
| `gene_openclaw_hub_start_cmd` | 启动命令 | `grep "openclaw hub start"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_hubs_start_verify` | 入门页面校验 | `openclaw:start:hubs:verify` |

---

## 📋 已验证事实

1. ✅ 配置目录：/var/lib/openclaw/hubs
2. ✅ 启动命令：openclaw hub start
3. ✅ 列表命令：openclaw hub list
4. ✅ 停止命令：openclaw hub stop

---

## 🟡 待补充

- [ ] Hub 创建详细步骤
- [ ] 停止命令参数用法
- [ ] Hub 配置文件格式

---

## 📚 来源

- **原始采样**: `raw/hubs-start-sample-20260422-0115.md`
- **官方文档**: https://docs.openclaw.ai/start/hubs

---

**最后更新**: 2026-04-22 01:15 GMT+8  
**维护者**: Red Agent Team
