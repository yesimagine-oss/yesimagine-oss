---
category: openclaw
created_at: '2026-04-22'
tags:
- gateway
- network-model
- verified
title: 网关网络模型
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/gateway/network-model"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 网关网络模型

**来源**: https://docs.openclaw.ai/gateway/network-model  
**验证时间**: 2026-04-22 02:25 GMT+8  
**状态**: 🟡 仅主页面，待补充配置语法与示例

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Gateway Network Model |
| **网络模式** | ✅ proxy, bridge, direct |
| **配置路径** | ✅ /etc/openclaw/gateway/network.yaml |
| **连接超时** | ✅ 30s default |
| **最大连接数** | ✅ 1024 |
| **配置语法** | ❌ 缺模式设置方法 |
| **配置示例** | ❌ 缺 yaml 样例 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_gateway_netmodel_title` | 网络模型标题 | `grep "Gateway Network Model"` |
| `gene_openclaw_gateway_netmode` | 网络模式 | `grep "proxy, bridge, direct"` |
| `gene_openclaw_gateway_netconfig_path` | 配置路径 | `grep "/etc/openclaw/gateway/network.yaml"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_gateway_netmodel_verify` | 网络模型校验 | `openclaw:gateway:network-model:verify` |

---

## 📋 已验证事实

1. ✅ 网络模式：proxy, bridge, direct
2. ✅ 配置路径：/etc/openclaw/gateway/network.yaml
3. ✅ 连接超时：30s default
4. ✅ 最大连接数：1024

---

## 🟡 待补充

- [ ] 网络模式配置语法
- [ ] 配置文件完整示例
- [ ] 最大连接数配置方法

---

## 📚 来源

- **原始采样**: `raw/gateway-network-model-sample-20260422-0225.md`
- **官方文档**: https://docs.openclaw.ai/gateway/network-model

---

**最后更新**: 2026-04-22 02:25 GMT+8  
**维护者**: Red Agent Team
