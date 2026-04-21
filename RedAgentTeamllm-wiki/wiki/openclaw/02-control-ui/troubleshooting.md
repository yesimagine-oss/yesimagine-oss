---
category: openclaw
created_at: '2026-04-22'
tags:
- troubleshooting
- channels
- verified
title: 通道排障指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/channels/troubleshooting"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 通道排障指南

**来源**: https://docs.openclaw.ai/channels/troubleshooting  
**验证时间**: 2026-04-22 00:55 GMT+8  
**状态**: 🟡 仅主页面，待补充排障命令

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Channels Troubleshooting |
| **常见故障** | ✅ Location channel not receiving updates |
| **检查项** | ✅ Check channel permissions |
| **日志路径** | ✅ /var/log/openclaw/channels.log |
| **排障命令** | ❌ 缺详细步骤 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_troubleshooting_title` | 排障文档标题 | `grep "Channels Troubleshooting"` |
| `gene_openclaw_troubleshooting_location_issue` | 位置通道典型故障 | `grep "Location channel not receiving updates"` |
| `gene_openclaw_channel_log_path` | 通道日志路径 | `grep "/var/log/openclaw/channels.log"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_troubleshooting_verify` | 排障页面校验 | `openclaw:channels:troubleshooting:verify` |

---

## 📋 已验证事实

1. ✅ 位置通道常见故障：未接收更新
2. ✅ 排障检查项：权限、webhook、服务重启、防火墙
3. ✅ 日志路径：/var/log/openclaw/channels.log

---

## 🟡 待补充

- [ ] webhook 配置校验命令
- [ ] 服务重启命令（systemctl）
- [ ] 防火墙检查命令

---

## 📚 来源

- **原始采样**: `raw/troubleshooting-sample-20260422-0055.md`
- **官方文档**: https://docs.openclaw.ai/channels/troubleshooting

---

**最后更新**: 2026-04-22 00:55 GMT+8  
**维护者**: Red Agent Team
