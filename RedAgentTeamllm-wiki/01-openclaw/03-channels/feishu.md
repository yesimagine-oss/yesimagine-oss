---
category: openclaw
created_at: '2026-04-21'
tags:
- channels
- feishu
- verified
title: 飞书通道配置
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/channels/feishu"
  captured_at: "2026-04-21"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "首页结构验证"
---

# 飞书通道配置

**来源**: https://docs.openclaw.ai/channels/feishu  
**验证时间**: 2026-04-21 18:10 GMT+8  
**状态**: 🟡 首页结构已验证，待深度采样

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档入口** | ✅ Feishu Channel |
| **Webhook 设置** | ✅ Webhook Setup |
| **消息格式** | ✅ Message Format |
| **机器人配置** | ✅ Bot Configuration |
| **排错模块** | ✅ Troubleshooting |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_feishu_channel_title` | 文档确认 | `grep -o "Feishu Channel"` |
| `gene_openclaw_feishu_webhook` | Webhook 配置 | `grep -o "Webhook Setup"` |
| `gene_openclaw_feishu_ts` | 排错模块 | `grep -o "Troubleshooting"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_feishu_verify` | 文档校验 | `openclaw:channels:feishu:verify` |

---

## 📋 已验证事实

1. ✅ 飞书通道文档入口存在
2. ✅ Webhook Setup 配置模块存在
3. ✅ Troubleshooting 排错模块存在

---

## 🟡 待验证内容

- [ ] Bot Configuration 机器人创建与权限
- [ ] Message Format 消息卡片格式、示例
- [ ] Webhook 地址获取、签名校验
- [ ] 排错步骤、测试方法

---

## 📚 来源

- **原始采样**: `raw/feishu-sample-20260421-1810.md`
- **官方文档**: https://docs.openclaw.ai/channels/feishu

---

**最后更新**: 2026-04-21 18:10 GMT+8  
**维护者**: Red Agent Team
