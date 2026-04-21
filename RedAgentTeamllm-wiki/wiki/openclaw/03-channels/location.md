---
category: openclaw
created_at: '2026-04-22'
tags:
- channels
- location
- verified
title: Location 通道配置
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/channels/location"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Location 通道配置

**来源**: https://docs.openclaw.ai/channels/location  
**验证时间**: 2026-04-22 00:42 GMT+8  
**状态**: 🟡 仅 L1 主页面，待深入二级配置

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档入口** | ✅ Location Channel |
| **支持渠道** | ✅ Telegram, WhatsApp, Matrix |
| **文本格式** | ✅ Pin/Named/Live (3 种) |
| **上下文字段** | ✅ 7 项 (LocationLat 等) |
| **配置模块** | ✅ Configuration (入口) |
| **完整配置** | ❌ 未深入二级锚点 |
| **测试命令** | ❌ 无 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_location_channel_identity` | 文档标识 | `grep "Location Channel"` |
| `gene_openclaw_location_supported_channels` | 支持渠道 | `grep -E "Telegram\|WhatsApp\|Matrix"` |
| `gene_openclaw_location_context_fields` | 上下文字段 | `grep -A 7 "Context fields"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_location_channel_validation` | 通道校验 | `openclaw:channels:location:validate` |

---

## 📋 已验证事实

1. ✅ 支持 Telegram/WhatsApp/Matrix 位置解析
2. ✅ 提供 3 种文本格式 (Pin/Named/Live)
3. ✅ 注入 7 项上下文字段

---

## 🟡 待补充

- [ ] 二级 #configuration 配置参数
- [ ] 实时位置解析逻辑
- [ ] 异常处理/排障 SOP

---

## 📚 来源

- **原始采样**: `raw/location-sample-20260422-0042.md`
- **官方文档**: https://docs.openclaw.ai/channels/location

---

**最后更新**: 2026-04-22 00:42 GMT+8  
**维护者**: Red Agent Team
