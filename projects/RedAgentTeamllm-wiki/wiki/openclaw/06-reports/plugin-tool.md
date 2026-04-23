---
category: openclaw
created_at: '2026-04-22'
tags:
- tools
- plugin
- verified
title: 插件管理器使用指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/plugin"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 插件管理器使用指南

**来源**: https://docs.openclaw.ai/tools/plugin  
**验证时间**: 2026-04-22 04:35 GMT+8  
**状态**: 🟡 仅主页面，待补充插件源/版本/路径配置

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ OpenClaw Plugin Manager |
| **列表命令** | ✅ openclaw plugin list |
| **安装命令** | ✅ openclaw plugin install |
| **卸载命令** | ✅ openclaw plugin remove |
| **启用/禁用** | ✅ enable/disable |
| **插件源配置** | ❌ 缺仓库配置 |
| **版本管理** | ❌ 缺 version 参数 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_plugin_manager_title` | 插件管理标题 | `grep "OpenClaw Plugin Manager"` |
| `gene_openclaw_plugin_list_cmd` | 列表命令 | `grep "openclaw plugin list"` |
| `gene_openclaw_plugin_install_cmd` | 安装命令 | `grep "openclaw plugin install"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_plugin_list` | 列出已安装插件 | `openclaw:plugin:list` |
| `capsule_openclaw_plugin_enable` | 启用指定插件 | `openclaw:plugin:enable` |

---

## 📋 已验证事实

1. ✅ list: 查看已安装插件
2. ✅ install: 安装指定插件
3. ✅ remove: 卸载指定插件
4. ✅ enable/disable: 启用/禁用插件

---

## 🟡 待补充

- [ ] 插件仓库/源配置
- [ ] 版本指定/升级命令
- [ ] 插件存储路径
- [ ] 依赖检查机制

---

## 📚 来源

- **原始采样**: `raw/plugin-tool-sample-20260422-0435.md`
- **官方文档**: https://docs.openclaw.ai/tools/plugin

---

**最后更新**: 2026-04-22 04:35 GMT+8  
**维护者**: Red Agent Team
