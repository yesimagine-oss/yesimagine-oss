---
category: openclaw
created_at: '2026-04-22'
tags:
- gateway
- configuration
- examples
- verified
title: Gateway 配置示例指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/gateway/configuration-examples"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Gateway 配置示例指南

**来源**: https://docs.openclaw.ai/gateway/configuration-examples  
**验证时间**: 2026-04-22 03:25 GMT+8  
**状态**: 🟡 仅主页面，待补充多路由/负载均衡/限流配置

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Gateway Configuration Examples |
| **基础配置示例** | ✅ listen/timeout/max_concurrent |
| **TLS 配置示例** | ✅ cert_file/key_file |
| **路由配置示例** | ✅ path/target/timeout |
| **多路由配置** | ❌ 缺示例 |
| **负载均衡** | ❌ 缺 upstream |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_gateway_config_examples_title` | 配置示例标题 | `grep "Gateway Configuration Examples"` |
| `gene_openclaw_gateway_basic_config` | 基础配置示例 | `grep -A 4 "Basic gateway config:"` |
| `gene_openclaw_gateway_tls_config` | TLS 配置示例 | `grep -A 6 "TLS-enabled config:"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_gateway_write_basic_config` | 生成基础配置 | `openclaw:gateway:config:write-basic` |
| `capsule_openclaw_gateway_configure_tls` | 配置 HTTPS | `openclaw:gateway:config:tls` |

---

## 📋 已验证事实

1. ✅ 基础配置：listen/timeout/max_concurrent
2. ✅ TLS 配置：cert_file/key_file
3. ✅ 路由配置：path/target/timeout

---

## 🟡 待补充

- [ ] 多路由转发配置
- [ ] 负载均衡配置
- [ ] 限流/熔断配置
- [ ] 完整 gateway.yaml 示例

---

## 📚 来源

- **原始采样**: `raw/gateway-config-examples-sample-20260422-0325.md`
- **官方文档**: https://docs.openclaw.ai/gateway/configuration-examples

---

**最后更新**: 2026-04-22 03:25 GMT+8  
**维护者**: Red Agent Team
