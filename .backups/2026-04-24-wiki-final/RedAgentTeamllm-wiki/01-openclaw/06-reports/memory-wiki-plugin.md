---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- memory
- wiki
- verified
title: Memory-Wiki 知识记忆插件指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/memory-wiki"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Memory-Wiki 知识记忆插件指南

**来源**: https://docs.openclaw.ai/plugins/memory-wiki  
**验证时间**: 2026-04-22 05:35 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/向量库/权限策略

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Memory Wiki Plugin |
| **核心用途** | ✅ persistent knowledge storage |
| **安装命令** | ✅ openclaw plugin install memory-wiki |
| **配置路径** | ✅ /etc/openclaw/plugins/memory-wiki.yaml |
| **核心能力** | ✅ ingest, query, embed, backup, sync |
| **完整配置** | ❌ 缺 YAML 示例 |
| **向量库对接** | ❌ 缺向量库配置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_memory_wiki_plugin_title` | 插件标题 | `grep "Memory Wiki Plugin"` |
| `gene_openclaw_memory_wiki_install_cmd` | 安装命令 | `grep "openclaw plugin install memory-wiki"` |
| `gene_openclaw_memory_wiki_config_path` | 配置路径 | `grep "/etc/openclaw/plugins/memory-wiki.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_memory_wiki` | 安装 Memory-Wiki | `openclaw:plugin:install:memory-wiki` |
| `capsule_openclaw_edit_memory_wiki_config` | 编辑配置 | `openclaw:plugin:memory-wiki:config:edit` |

---

## 📋 已验证事实

1. ✅ 用途：persistent knowledge storage & semantic wiki
2. ✅ 安装：openclaw plugin install memory-wiki
3. ✅ 配置：/etc/openclaw/plugins/memory-wiki.yaml
4. ✅ 能力：ingest, query, embed, backup, sync

---

## 🟡 待补充

- [ ] 完整 YAML 配置示例
- [ ] 向量数据库对接配置
- [ ] 数据导入导出格式
- [ ] 权限与隔离策略

---

## 📚 来源

- **原始采样**: `raw/memory-wiki-plugin-sample-20260422-0535.md`
- **官方文档**: https://docs.openclaw.ai/plugins/memory-wiki

---

**最后更新**: 2026-04-22 05:35 GMT+8  
**维护者**: Red Agent Team
