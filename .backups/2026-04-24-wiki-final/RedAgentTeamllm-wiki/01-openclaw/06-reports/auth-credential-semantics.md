---
category: openclaw
created_at: '2026-04-22'
tags:
- auth
- credential
- security
- verified
title: 凭证语义与生命周期指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/auth-credential-semantics"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 凭证语义与生命周期指南

**来源**: https://docs.openclaw.ai/auth-credential-semantics  
**验证时间**: 2026-04-22 03:45 GMT+8  
**状态**: 🟡 仅主页面，待补充配置示例与轮换策略

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Auth Credential Semantics |
| **凭证类型** | ✅ static, dynamic, ephemeral |
| **静态凭证** | ✅ permanent, manually managed |
| **动态凭证** | ✅ TTL-enabled, auto-rotated |
| **临时凭证** | ✅ short-lived, session-bound |
| **配置示例** | ❌ 缺 YAML |
| **轮换策略** | ❌ 缺 rotation_interval |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_auth_cred_semantics_title` | 凭证语义标题 | `grep "Auth Credential Semantics"` |
| `gene_openclaw_credential_types` | 凭证类型 | `grep "static, dynamic, ephemeral"` |
| `gene_openclaw_dynamic_credential` | 动态凭证特性 | `grep "TTL-enabled, auto-rotated"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_credential_type_check` | 查看凭证类型 | `openclaw:credential:type:check` |

---

## 📋 已验证事实

1. ✅ 三类凭证：static, dynamic, ephemeral
2. ✅ 静态凭证：permanent, manually managed
3. ✅ 动态凭证：TTL-enabled, auto-rotated
4. ✅ 临时凭证：short-lived, session-bound

---

## 🟡 待补充

- [ ] 各凭证类型配置示例
- [ ] 轮换策略配置 (rotation_interval)
- [ ] 过期策略配置 (expires_in)
- [ ] 权限范围绑定 (scope)

---

## 📚 来源

- **原始采样**: `raw/auth-credential-semantics-sample-20260422-0345.md`
- **官方文档**: https://docs.openclaw.ai/auth-credential-semantics

---

**最后更新**: 2026-04-22 03:45 GMT+8  
**维护者**: Red Agent Team
