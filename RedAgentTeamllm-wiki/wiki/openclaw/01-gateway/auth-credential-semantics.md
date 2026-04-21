---
category: openclaw
created_at: '2026-04-22'
tags:
- auth
- credentials
- verified
title: 凭证语义规范
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

# 凭证语义规范

**来源**: https://docs.openclaw.ai/auth-credential-semantics  
**验证时间**: 2026-04-22 01:55 GMT+8  
**状态**: 🟡 仅主页面，待补充动态凭证与配置示例

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Auth Credential Semantics |
| **凭证类型** | ✅ static, dynamic, federated |
| **静态凭证路径** | ✅ /etc/openclaw/credentials.yaml |
| **轮换周期** | ✅ 1h default |
| **验证策略** | ✅ deny_on_failure |
| **动态凭证规则** | ❌ 缺生成逻辑 |
| **配置示例** | ❌ 缺 yaml 样例 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_auth_cred_semantics_title` | 凭证语义标题 | `grep "Auth Credential Semantics"` |
| `gene_openclaw_static_cred_path` | 静态凭证路径 | `grep "/etc/openclaw/credentials.yaml"` |
| `gene_openclaw_cred_validation_policy` | 验证策略 | `grep "deny_on_failure"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_auth_cred_verify` | 凭证语义校验 | `openclaw:auth-credential-semantics:verify` |

---

## 📋 已验证事实

1. ✅ 凭证类型：static, dynamic, federated
2. ✅ 静态凭证路径：/etc/openclaw/credentials.yaml
3. ✅ 轮换周期：1h default
4. ✅ 验证策略：deny_on_failure

---

## 🟡 待补充

- [ ] 动态凭证生成逻辑
- [ ] 轮换周期配置方法
- [ ] credentials.yaml 配置示例

---

## 📚 来源

- **原始采样**: `raw/auth-credential-semantics-sample-20260422-0155.md`
- **官方文档**: https://docs.openclaw.ai/auth-credential-semantics

---

**最后更新**: 2026-04-22 01:55 GMT+8  
**维护者**: Red Agent Team
