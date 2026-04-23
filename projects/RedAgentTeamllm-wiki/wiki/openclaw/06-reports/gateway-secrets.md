---
category: openclaw
created_at: '2026-04-22'
tags:
- gateway
- secrets
- security
- verified
title: Gateway 密钥管理指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/gateway/secrets"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Gateway 密钥管理指南

**来源**: https://docs.openclaw.ai/gateway/secrets  
**验证时间**: 2026-04-22 03:55 GMT+8  
**状态**: 🟡 仅主页面，待补充 Vault 集成与生产级安全配置

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Gateway Secrets Management |
| **密钥后端** | ✅ file, env, vault |
| **文件路径** | ✅ /etc/openclaw/secrets.yaml |
| **环境变量** | ✅ OPENCLAW_* |
| **引用语法** | ✅ ${FILE:...} / ${ENV:...} |
| **Vault 配置** | ❌ 缺地址/令牌 |
| **密钥加密** | ❌ 缺加密配置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_gateway_secrets_title` | 密钥管理标题 | `grep "Gateway Secrets Management"` |
| `gene_openclaw_secret_backends` | 密钥后端类型 | `grep "file, env, vault"` |
| `gene_openclaw_file_secret_path` | 文件密钥路径 | `grep "/etc/openclaw/secrets.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_create_secrets_file` | 创建密钥文件 | `openclaw:secrets:file:create` |
| `capsule_openclaw_secure_secrets_file` | 安全加固密钥文件 | `openclaw:secrets:file:secure` |

---

## 📋 已验证事实

1. ✅ 三种后端：file, env, vault
2. ✅ 文件路径：/etc/openclaw/secrets.yaml
3. ✅ 环境变量：OPENCLAW_*
4. ✅ 引用语法：${FILE:...} / ${ENV:...}

---

## 🟡 待补充

- [ ] Vault 集成配置
- [ ] 密钥文件权限规范
- [ ] 密钥加密存储
- [ ] 密钥热重载配置

---

## 📚 来源

- **原始采样**: `raw/gateway-secrets-sample-20260422-0355.md`
- **官方文档**: https://docs.openclaw.ai/gateway/secrets

---

**最后更新**: 2026-04-22 03:55 GMT+8  
**维护者**: Red Agent Team
