---
category: openclaw
created_at: '2026-04-21'
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
  captured_at: "2026-04-21"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "部分覆盖"
---

# Location 通道配置

**来源**: https://docs.openclaw.ai/channels/location  
**验证时间**: 2026-04-21 19:12 GMT+8  
**状态**: 🟡 部分覆盖，待补充鉴权/测试

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档入口** | ✅ Location Channel |
| **支持渠道** | ✅ Telegram, WhatsApp, Matrix |
| **文本格式** | ✅ Pin/Named/Live (3 种) |
| **上下文字段** | ✅ 7 项 (LocationLat 等) |
| **鉴权方法** | ❌ 未提取 |
| **测试命令** | ❌ 未提取 |

---

## 🧬 关联资产

### Genes (4 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_location_channel_basic` | 基础标识 | `grep "Location Channel"` |
| `gene_openclaw_location_supported_platforms` | 支持平台 | `grep -E "Telegram\|WhatsApp\|Matrix"` |
| `gene_openclaw_location_text_formats` | 文本格式 | `grep -A 10 "Text formatting"` |
| `gene_openclaw_location_context_fields` | 上下文字段 | `grep -A 7 "Context fields"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_location_channel_verify` | 通道校验 | `openclaw:channels:location:verify` |

---

## 📋 已验证事实

1. ✅ 支持 Telegram/WhatsApp/Matrix 位置解析
2. ✅ 提供 3 种文本格式 (Pin/Named/Live)
3. ✅ 注入 7 项上下文字段

---

## 🟡 待补充

- [ ] 鉴权方法
- [ ] 测试命令

---

## 📚 来源

- **原始采样**: `raw/location-sample-20260421-1912.md`
- **官方文档**: https://docs.openclaw.ai/channels/location

---

**最后更新**: 2026-04-21 19:12 GMT+8  
**维护者**: Red Agent Team
