---
category: openclaw
created_at: '2026-04-22'
tags:
- web
- webchat
- verified
title: WebChat 网页交互界面指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/web/webchat"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# WebChat 网页交互界面指南

**来源**: https://docs.openclaw.ai/web/webchat  
**验证时间**: 2026-04-22 02:55 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置示例与高级选项

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ OpenClaw WebChat Interface |
| **访问地址** | ✅ http://localhost:8080/webchat |
| **认证请求头** | ✅ X-OpenClaw-API-Key |
| **配置文件路径** | ✅ /etc/openclaw/webchat.yaml |
| **启用开关** | ✅ webchat.enabled: true |
| **完整配置示例** | ❌ 缺 yaml 结构 |
| **CORS 配置** | ❌ 缺域名限制 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_webchat_title` | WebChat 页面标题 | `grep "OpenClaw WebChat Interface"` |
| `gene_openclaw_webchat_url` | 访问地址 | `grep "http://localhost:8080/webchat"` |
| `gene_openclaw_webchat_config_path` | 配置路径 | `grep "/etc/openclaw/webchat.yaml"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_webchat_verify` | WebChat 可访问性校验 | `openclaw:web:webchat:verify` |

---

## 📋 已验证事实

1. ✅ 访问地址：http://localhost:8080/webchat
2. ✅ 认证请求头：X-OpenClaw-API-Key
3. ✅ 配置文件：/etc/openclaw/webchat.yaml
4. ✅ 启用开关：webchat.enabled: true

---

## 🟡 待补充

- [ ] webchat.yaml 完整配置示例
- [ ] 会话持久化配置
- [ ] CORS / 域名访问限制
- [ ] 主题/界面定制选项

---

## 📚 来源

- **原始采样**: `raw/webchat-sample-20260422-0255.md`
- **官方文档**: https://docs.openclaw.ai/web/webchat

---

**最后更新**: 2026-04-22 02:55 GMT+8  
**维护者**: Red Agent Team
