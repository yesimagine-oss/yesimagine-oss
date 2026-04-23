---
category: openclaw
created_at: '2026-04-22'
tags:
- gateway
- authentication
- verified
title: 网关认证配置
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

# 网关认证配置

**来源**: https://docs.openclaw.ai/gateway/authentication  
**验证时间**: 2026-04-22 01:45 GMT+8  
**状态**: 🟡 仅主页面，待补充密钥生成与配置示例

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Gateway Authentication |
| **认证方式** | ✅ API Key authentication |
| **请求头** | ✅ X-OpenClaw-API-Key |
| **配置路径** | ✅ /etc/openclaw/gateway/auth.yaml |
| **禁用开关** | ✅ auth.enabled: false |
| **密钥生成** | ❌ 缺步骤 |
| **配置示例** | ❌ 缺样例 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_gateway_auth_title` | 认证文档标题 | `grep "Gateway Authentication"` |
| `gene_openclaw_gateway_api_header` | 请求头 | `grep "X-OpenClaw-API-Key"` |
| `gene_openclaw_gateway_auth_config` | 配置路径 | `grep "/etc/openclaw/gateway/auth.yaml"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_gateway_auth_verify` | 认证页面校验 | `openclaw:gateway:authentication:verify` |

---

## 📋 已验证事实

1. ✅ 认证方式：API Key
2. ✅ 请求头：X-OpenClaw-API-Key
3. ✅ 配置路径：/etc/openclaw/gateway/auth.yaml
4. ✅ 禁用开关：auth.enabled: false

---

## 🟡 待补充

- [ ] API Key 生成方法
- [ ] auth.yaml 配置示例
- [ ] 认证失败排障

---

## 📚 来源

- **原始采样**: `raw/gateway-authentication-sample-20260422-0145.md`
- **官方文档**: https://docs.openclaw.ai/gateway/authentication

---

**最后更新**: 2026-04-22 01:45 GMT+8  
**维护者**: Red Agent Team
