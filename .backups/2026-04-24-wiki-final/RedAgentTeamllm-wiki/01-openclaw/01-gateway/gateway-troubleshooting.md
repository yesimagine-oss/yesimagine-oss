---
category: openclaw
created_at: '2026-04-22'
tags:
- gateway
- troubleshooting
- verified
title: 网关排障指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/gateway/troubleshooting"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 网关排障指南

**来源**: https://docs.openclaw.ai/gateway/troubleshooting  
**验证时间**: 2026-04-22 01:35 GMT+8  
**状态**: 🟡 仅主页面，待补充端口检查命令与配置路径

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Gateway Troubleshooting |
| **无法启动故障** | ✅ Gateway not starting |
| **端口检查** | ✅ Check port 8080 |
| **日志路径** | ✅ /var/log/openclaw/gateway.log |
| **重启命令** | ✅ systemctl restart openclaw-gateway |
| **端口检查命令** | ❌ 缺具体命令 |
| **配置路径** | ❌ 缺配置文件位置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_gateway_ts_title` | 排障文档标题 | `grep "Gateway Troubleshooting"` |
| `gene_openclaw_gateway_log_path` | 日志路径 | `grep "/var/log/openclaw/gateway.log"` |
| `gene_openclaw_gateway_restart_cmd` | 重启命令 | `grep "systemctl restart openclaw-gateway"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_gateway_ts_verify` | 排障页面校验 | `openclaw:gateway:troubleshooting:verify` |

---

## 📋 已验证事实

1. ✅ 日志路径：/var/log/openclaw/gateway.log
2. ✅ 重启命令：systemctl restart openclaw-gateway
3. ✅ 端口检查：8080
4. ✅ 核心故障：Gateway not starting

---

## 🟡 待补充

- [ ] 端口检查命令（ss/lsof）
- [ ] 网关配置文件路径
- [ ] 启动失败详细原因

---

## 📚 来源

- **原始采样**: `raw/gateway-troubleshooting-sample-20260422-0135.md`
- **官方文档**: https://docs.openclaw.ai/gateway/troubleshooting

---

**最后更新**: 2026-04-22 01:35 GMT+8  
**维护者**: Red Agent Team
