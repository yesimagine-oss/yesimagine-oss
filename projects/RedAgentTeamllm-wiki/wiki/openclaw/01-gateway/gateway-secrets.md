---
category: openclaw
created_at: '2026-04-22'
tags:
- gateway
- secrets
- verified
title: 网关密钥管理
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

# 网关密钥管理

**来源**: https://docs.openclaw.ai/gateway/secrets  
**验证时间**: 2026-04-22 02:05 GMT+8  
**状态**: 🟡 仅主页面，待补充配置示例与加密命令

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Gateway Secrets Management |
| **密钥存储路径** | ✅ /etc/openclaw/secrets.yaml |
| **加密算法** | ✅ AES-256-GCM |
| **重载命令** | ✅ systemctl reload openclaw-gateway |
| **作用域类型** | ✅ gateway, channel, global |
| **配置示例** | ❌ 缺 yaml 样例 |
| **加密命令** | ❌ 缺工具用法 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_gateway_secrets_title` | 密钥管理标题 | `grep "Gateway Secrets Management"` |
| `gene_openclaw_secrets_config_path` | 密钥配置路径 | `grep "/etc/openclaw/secrets.yaml"` |
| `gene_openclaw_secrets_reload_cmd` | 重载命令 | `grep "systemctl reload openclaw-gateway"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_gateway_secrets_verify` | 密钥页面校验 | `openclaw:gateway:secrets:verify` |

---

## 📋 已验证事实

1. ✅ 密钥存储路径：/etc/openclaw/secrets.yaml
2. ✅ 加密算法：AES-256-GCM
3. ✅ 重载命令：systemctl reload openclaw-gateway
4. ✅ 作用域类型：gateway, channel, global

---

## 🟡 待补充

- [ ] secrets.yaml 配置示例
- [ ] 作用域配置语法
- [ ] 密钥加密工具命令

---

## 📚 来源

- **原始采样**: `raw/gateway-secrets-sample-20260422-0205.md`
- **官方文档**: https://docs.openclaw.ai/gateway/secrets

---

**最后更新**: 2026-04-22 02:05 GMT+8  
**维护者**: Red Agent Team
