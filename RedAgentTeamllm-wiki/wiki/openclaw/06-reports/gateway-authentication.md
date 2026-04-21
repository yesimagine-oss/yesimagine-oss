---
category: openclaw
created_at: '2026-04-22'
tags:
- gateway
- authentication
- security
- verified
title: Gateway 鉴权配置指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/gateway/authentication"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Gateway 鉴权配置指南

**来源**: https://docs.openclaw.ai/gateway/authentication  
**验证时间**: 2026-04-22 03:35 GMT+8  
**状态**: 🟡 仅主页面，待补充 OAuth2/多鉴权/白名单配置

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Gateway Authentication |
| **鉴权方法** | ✅ api-key, jwt, oauth2 |
| **默认方法** | ✅ api-key |
| **API Key 头** | ✅ X-OpenClaw-Api-Key |
| **JWT 配置** | ✅ secret/issuer |
| **OAuth2 配置** | ❌ 缺示例 |
| **白名单配置** | ❌ 缺 skip_paths |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_gateway_auth_title` | 鉴权页面标题 | `grep "Gateway Authentication"` |
| `gene_openclaw_gateway_auth_methods` | 鉴权方法 | `grep "api-key, jwt, oauth2"` |
| `gene_openclaw_gateway_api_key_header` | API Key 请求头 | `grep "X-OpenClaw-Api-Key"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_gateway_configure_basic_auth` | API Key 鉴权 | `openclaw:gateway:auth:api-key` |
| `capsule_openclaw_gateway_configure_jwt_auth` | JWT 鉴权 | `openclaw:gateway:auth:jwt` |

---

## 📋 已验证事实

1. ✅ 三种鉴权方法：api-key, jwt, oauth2
2. ✅ 默认方法：api-key
3. ✅ API Key 请求头：X-OpenClaw-Api-Key
4. ✅ JWT 配置：secret/issuer

---

## 🟡 待补充

- [ ] OAuth2 配置示例
- [ ] 多鉴权方法共存配置
- [ ] 白名单配置 (skip_paths)
- [ ] 鉴权失败响应配置

---

## 📚 来源

- **原始采样**: `raw/gateway-auth-sample-20260422-0335.md`
- **官方文档**: https://docs.openclaw.ai/gateway/authentication

---

**最后更新**: 2026-04-22 03:35 GMT+8  
**维护者**: Red Agent Team
