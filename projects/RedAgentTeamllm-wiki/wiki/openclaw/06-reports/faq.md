---
category: openclaw
created_at: '2026-04-22'
tags:
- faq
- help
- verified
title: FAQ 常见问题
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/help/faq"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# FAQ 常见问题

**来源**: https://docs.openclaw.ai/help/faq  
**验证时间**: 2026-04-22 01:25 GMT+8  
**状态**: 🟡 仅主页面，待补充重启命令与更新步骤

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **FAQ 标题** | ✅ OpenClaw Frequently Asked Questions |
| **日志路径** | ✅ /var/log/openclaw/ |
| **重启问题** | ✅ How to restart OpenClaw services? |
| **更新问题** | ✅ How to update OpenClaw to latest version? |
| **重启命令** | ❌ 缺具体命令 |
| **更新步骤** | ❌ 缺流程 |

---

## 🧬 关联资产

### Genes (2 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_faq_title` | FAQ 页面标题 | `grep "OpenClaw Frequently Asked Questions"` |
| `gene_openclaw_faq_log_path` | 日志存储路径 | `grep "/var/log/openclaw/"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_faq_verify` | FAQ 页面校验 | `openclaw:help:faq:verify` |

---

## 📋 已验证事实

1. ✅ 日志路径：/var/log/openclaw/
2. ✅ 常见问题：重启服务、版本更新、日志位置

---

## 🟡 待补充

- [ ] 服务重启具体命令
- [ ] 版本更新步骤
- [ ] 日志查看命令

---

## 📚 来源

- **原始采样**: `raw/faq-sample-20260422-0125.md`
- **官方文档**: https://docs.openclaw.ai/help/faq

---

**最后更新**: 2026-04-22 01:25 GMT+8  
**维护者**: Red Agent Team
