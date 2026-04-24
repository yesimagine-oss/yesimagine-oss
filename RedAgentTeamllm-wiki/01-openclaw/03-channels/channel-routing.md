---
category: openclaw
created_at: '2026-04-22'
tags:
- channels
- routing
- verified
title: 通道路由配置
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/channels/channel-routing"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 通道路由配置

**来源**: https://docs.openclaw.ai/channels/channel-routing  
**验证时间**: 2026-04-22 01:05 GMT+8  
**状态**: 🟡 仅主页面，待补充路由规则与配置示例

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Channel Routing |
| **位置通道路由** | ✅ Location channel routing rules |
| **配置文件路径** | ✅ /etc/openclaw/routing.yaml |
| **重启命令** | ✅ systemctl restart openclaw-channels |
| **路由规则** | ❌ 缺完整规则 |
| **配置示例** | ❌ 缺 yaml 示例 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_channel_routing_title` | 路由文档标题 | `grep "Channel Routing"` |
| `gene_openclaw_routing_config_path` | 配置文件路径 | `grep "/etc/openclaw/routing.yaml"` |
| `gene_openclaw_routing_restart_cmd` | 重启命令 | `grep "systemctl restart openclaw-channels"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_channel_routing_verify` | 路由页面校验 | `openclaw:channels:routing:verify` |

---

## 📋 已验证事实

1. ✅ 配置文件路径：/etc/openclaw/routing.yaml
2. ✅ 重启命令：systemctl restart openclaw-channels
3. ✅ 位置通道路由规则存在

---

## 🟡 待补充

- [ ] 通道类型路由逻辑
- [ ] fallback 路由规则
- [ ] routing.yaml 配置示例

---

## 📚 来源

- **原始采样**: `raw/channel-routing-sample-20260422-0105.md`
- **官方文档**: https://docs.openclaw.ai/channels/channel-routing

---

**最后更新**: 2026-04-22 01:05 GMT+8  
**维护者**: Red Agent Team
