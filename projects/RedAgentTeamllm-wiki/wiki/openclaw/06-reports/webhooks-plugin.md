---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- webhooks
- events
- verified
title: Webhooks 事件回调插件指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/webhooks"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Webhooks 事件回调插件指南

**来源**: https://docs.openclaw.ai/plugins/webhooks  
**验证时间**: 2026-04-22 05:15 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/payload/重试策略

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Webhooks Plugin |
| **核心用途** | ✅ event-driven HTTP callbacks |
| **安装命令** | ✅ openclaw plugin install webhooks |
| **配置路径** | ✅ /etc/openclaw/plugins/webhooks.yaml |
| **支持事件** | ✅ request, response, error, plugin-lifecycle |
| **完整配置** | ❌ 缺 YAML 示例 |
| **Payload 结构** | ❌ 缺数据格式 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_webhooks_plugin_title` | 插件标题 | `grep "Webhooks Plugin"` |
| `gene_openclaw_webhooks_install_cmd` | 安装命令 | `grep "openclaw plugin install webhooks"` |
| `gene_openclaw_webhooks_config_path` | 配置路径 | `grep "/etc/openclaw/plugins/webhooks.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_webhooks` | 安装 Webhooks 插件 | `openclaw:plugin:install:webhooks` |
| `capsule_openclaw_edit_webhooks_config` | 编辑配置 | `openclaw:plugin:webhooks:config:edit` |

---

## 📋 已验证事实

1. ✅ 用途：event-driven HTTP callbacks for gateway events
2. ✅ 安装：openclaw plugin install webhooks
3. ✅ 配置：/etc/openclaw/plugins/webhooks.yaml
4. ✅ 支持事件：request, response, error, plugin-lifecycle

---

## 🟡 待补充

- [ ] 完整 YAML 配置示例
- [ ] 事件 payload 结构
- [ ] 重试/超时配置
- [ ] HMAC 签名校验

---

## 📚 来源

- **原始采样**: `raw/webhooks-plugin-sample-20260422-0515.md`
- **官方文档**: https://docs.openclaw.ai/plugins/webhooks

---

**最后更新**: 2026-04-22 05:15 GMT+8  
**维护者**: Red Agent Team
