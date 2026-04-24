---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- sdk
- migration
- verified
title: SDK 插件迁移指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/sdk-migration"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# SDK 插件迁移指南

**来源**: https://docs.openclaw.ai/plugins/sdk-migration  
**验证时间**: 2026-04-22 06:25 GMT+8  
**状态**: 🟡 仅主页面，待补充接口差异/报错排查/回滚流程

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ SDK Migration Guide |
| **迁移目的** | ✅ v1 → v2 SDK ABI compatible |
| **迁移命令** | ✅ openclaw plugin migrate |
| **自动备份** | ✅ .backup before migration |
| **验证命令** | ✅ openclaw plugin verify |
| **接口差异** | ❌ 缺 breaking changes |
| **回滚流程** | ❌ 缺恢复步骤 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_sdk_migration_title` | 迁移文档标题 | `grep "SDK Migration Guide"` |
| `gene_openclaw_plugin_migrate_cmd` | 迁移命令 | `grep "openclaw plugin migrate"` |
| `gene_openclaw_plugin_verify_cmd` | 验证命令 | `grep "openclaw plugin verify"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_plugin_migrate` | 执行插件迁移 | `openclaw:plugin:migrate` |
| `capsule_openclaw_plugin_verify` | 验证迁移后插件 | `openclaw:plugin:verify` |

---

## 📋 已验证事实

1. ✅ 目的：migrate v1 plugins to v2 SDK ABI compatible format
2. ✅ 迁移：openclaw plugin migrate ./input.so ./output.so
3. ✅ 备份：auto-create .backup before migration
4. ✅ 验证：openclaw plugin verify ./plugin.so

---

## 🟡 待补充

- [ ] v1/v2 接口差异清单
- [ ] 迁移错误排查指南
- [ ] 批量迁移脚本
- [ ] 回滚操作流程

---

## 📚 来源

- **原始采样**: `raw/sdk-migration-sample-20260422-0625.md`
- **官方文档**: https://docs.openclaw.ai/plugins/sdk-migration

---

**最后更新**: 2026-04-22 06:25 GMT+8  
**维护者**: Red Agent Team
