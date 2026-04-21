---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- community
- verified
title: 社区插件注册表指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/community"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 社区插件注册表指南

**来源**: https://docs.openclaw.ai/plugins/community  
**验证时间**: 2026-04-22 04:45 GMT+8  
**状态**: 🟡 仅主页面，待补充插件配置/版本/依赖说明

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Community Plugins Registry |
| **仓库地址** | ✅ github.com/openclaw/community-plugins |
| **可用插件** | ✅ 4 个 (auth-proxy/rate-limiter 等) |
| **安装语法** | ✅ community/<plugin-name> |
| **贡献方式** | ✅ PR to GitHub |
| **插件配置** | ❌ 缺 YAML 示例 |
| **版本兼容** | ❌ 缺版本规则 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_community_plugins_title` | 社区插件标题 | `grep "Community Plugins Registry"` |
| `gene_openclaw_community_plugin_install_syntax` | 安装格式 | `grep "openclaw plugin install community/"` |
| `gene_openclaw_community_plugin_list` | 插件清单 | `grep "auth-proxy, request-transformer"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_community_rate_limiter` | 安装限流插件 | `openclaw:plugin:install:community:rate-limiter` |
| `capsule_openclaw_install_community_auth_proxy` | 安装认证代理插件 | `openclaw:plugin:install:community:auth-proxy` |

---

## 📋 已验证事实

1. ✅ 仓库：https://github.com/openclaw/community-plugins
2. ✅ 插件：auth-proxy, request-transformer, rate-limiter, logging-ext
3. ✅ 安装：openclaw plugin install community/<name>
4. ✅ 贡献：PR to GitHub repository

---

## 🟡 待补充

- [ ] 各插件配置 YAML 示例
- [ ] 版本兼容性规则
- [ ] 插件依赖要求
- [ ] 更新/升级命令

---

## 📚 来源

- **原始采样**: `raw/community-plugins-sample-20260422-0445.md`
- **官方文档**: https://docs.openclaw.ai/plugins/community

---

**最后更新**: 2026-04-22 04:45 GMT+8  
**维护者**: Red Agent Team
