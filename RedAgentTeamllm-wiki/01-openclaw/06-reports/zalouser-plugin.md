---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- user-management
- rbac
- verified
title: Zalouser 用户管理插件指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/zalouser"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Zalouser 用户管理插件指南

**来源**: https://docs.openclaw.ai/plugins/zalouser  
**验证时间**: 2026-04-22 05:45 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/OAuth-LDAP/审计日志

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Zalouser User Management Plugin |
| **核心用途** | ✅ centralized identity & access control |
| **安装命令** | ✅ openclaw plugin install zalouser |
| **配置路径** | ✅ /etc/openclaw/plugins/zalouser.yaml |
| **核心功能** | ✅ auth, rbac, profile, session, audit |
| **完整配置** | ❌ 缺 YAML 示例 |
| **OAuth/LDAP** | ❌ 缺第三方认证 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_zalouser_plugin_title` | 插件标题 | `grep "Zalouser User Management Plugin"` |
| `gene_openclaw_zalouser_install_cmd` | 安装命令 | `grep "openclaw plugin install zalouser"` |
| `gene_openclaw_zalouser_config_path` | 配置路径 | `grep "/etc/openclaw/plugins/zalouser.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_zalouser` | 安装用户管理插件 | `openclaw:plugin:install:zalouser` |
| `capsule_openclaw_edit_zalouser_config` | 编辑配置 | `openclaw:plugin:zalouser:config:edit` |

---

## 📋 已验证事实

1. ✅ 用途：centralized user identity & access control
2. ✅ 安装：openclaw plugin install zalouser
3. ✅ 配置：/etc/openclaw/plugins/zalouser.yaml
4. ✅ 功能：auth, rbac, user-profile, session, audit-log

---

## 🟡 待补充

- [ ] 完整 YAML 配置示例
- [ ] OAuth/LDAP 第三方认证对接
- [ ] 会话存储/过期策略
- [ ] 审计日志格式与存储

---

## 📚 来源

- **原始采样**: `raw/zalouser-plugin-sample-20260422-0545.md`
- **官方文档**: https://docs.openclaw.ai/plugins/zalouser

---

**最后更新**: 2026-04-22 05:45 GMT+8  
**维护者**: Red Agent Team
