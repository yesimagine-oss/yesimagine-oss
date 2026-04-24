---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- bundles
- verified
title: 插件捆绑包使用指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/bundles"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 插件捆绑包使用指南

**来源**: https://docs.openclaw.ai/plugins/bundles  
**验证时间**: 2026-04-22 04:55 GMT+8  
**状态**: 🟡 仅主页面，待补充完整包明细/配置模板/升级命令

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Plugin Bundles & Preset Collections |
| **捆绑包定义** | ✅ pre-configured plugin set |
| **可用捆绑包** | ✅ security, gateway, observability, devkit |
| **安装语法** | ✅ bundle/<bundle-name> |
| **security 包** | ✅ auth-proxy, rate-limiter, secrets-scanner |
| **gateway 包** | ❌ 缺明细 |
| **配置模板** | ❌ 缺预置配置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_plugin_bundles_title` | 捆绑包标题 | `grep "Plugin Bundles & Preset Collections"` |
| `gene_openclaw_bundle_install_syntax` | 安装语法 | `grep "openclaw plugin install bundle/"` |
| `gene_openclaw_security_bundle_content` | security 包内容 | `grep "security bundle: auth-proxy"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_security_bundle` | 安装安全包 | `openclaw:bundle:install:security` |
| `capsule_openclaw_install_observability_bundle` | 安装可观测性包 | `openclaw:bundle:install:observability` |

---

## 📋 已验证事实

1. ✅ 4 大捆绑包：security, gateway, observability, devkit
2. ✅ security 包：auth-proxy, rate-limiter, secrets-scanner
3. ✅ 安装命令：openclaw plugin install bundle/<name>

---

## 🟡 待补充

- [ ] gateway/observability/devkit 包明细
- [ ] 捆绑包配置模板
- [ ] bundle update/remove 命令
- [ ] 自定义捆绑包规范

---

## 📚 来源

- **原始采样**: `raw/plugin-bundles-sample-20260422-0455.md`
- **官方文档**: https://docs.openclaw.ai/plugins/bundles

---

**最后更新**: 2026-04-22 04:55 GMT+8  
**维护者**: Red Agent Team
