---
category: openclaw
created_at: '2026-04-22'
tags:
- network
- configuration
- verified
title: 网络配置
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/network"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 网络配置

**来源**: https://docs.openclaw.ai/network  
**验证时间**: 2026-04-22 02:15 GMT+8  
**状态**: 🟡 仅主页面，待补充配置示例与 TLS 配置

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ OpenClaw Network Configuration |
| **监听地址** | ✅ 0.0.0.0 |
| **默认端口** | ✅ 8080 |
| **配置路径** | ✅ /etc/openclaw/network.yaml |
| **防火墙命令** | ✅ firewall-cmd --add-port=8080/tcp |
| **配置示例** | ❌ 缺 yaml 样例 |
| **TLS 配置** | ❌ 缺 HTTPS 选项 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_network_title` | 网络配置标题 | `grep "OpenClaw Network Configuration"` |
| `gene_openclaw_network_config_path` | 配置路径 | `grep "/etc/openclaw/network.yaml"` |
| `gene_openclaw_network_default_port` | 默认端口 | `grep "8080"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_network_verify` | 网络配置校验 | `openclaw:network:verify` |

---

## 📋 已验证事实

1. ✅ 监听地址：0.0.0.0
2. ✅ 默认端口：8080
3. ✅ 配置路径：/etc/openclaw/network.yaml
4. ✅ 防火墙命令：firewall-cmd --add-port=8080/tcp

---

## 🟡 待补充

- [ ] network.yaml 配置示例
- [ ] 防火墙永久开放命令
- [ ] TLS/HTTPS 配置项

---

## 📚 来源

- **原始采样**: `raw/network-sample-20260422-0215.md`
- **官方文档**: https://docs.openclaw.ai/network

---

**最后更新**: 2026-04-22 02:15 GMT+8  
**维护者**: Red Agent Team
