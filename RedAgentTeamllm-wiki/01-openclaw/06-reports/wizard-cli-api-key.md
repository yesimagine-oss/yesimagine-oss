---
category: openclaw
created_at: '2026-04-22'
tags:
- wizard
- cli
- api-key
- verified
title: Wizard CLI API Key 管理指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/start/wizard-cli-reference#api-key-generic"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Wizard CLI API Key 管理指南

**来源**: https://docs.openclaw.ai/start/wizard-cli-reference#api-key-generic  
**验证时间**: 2026-04-22 02:45 GMT+8  
**状态**: 🟡 仅主页面，待补充高级参数与权限配置

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Wizard CLI Reference - API Key Generic |
| **生成命令** | ✅ `openclaw wizard api-key generate` |
| **列表命令** | ✅ `openclaw wizard api-key list` |
| **吊销命令** | ✅ `openclaw wizard api-key revoke <key-id>` |
| **存储路径** | ✅ `~/.openclaw/api-keys.yaml` |
| **过期参数** | ❌ 缺 --ttl |
| **权限配置** | ❌ 缺 scope |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_wizard_cli_api_key_title` | CLI 页面标题 | `grep "Wizard CLI Reference - API Key Generic"` |
| `gene_openclaw_api_key_generate_cmd` | 生成命令 | `grep "openclaw wizard api-key generate"` |
| `gene_openclaw_api_key_store_path` | 存储路径 | `grep "~/.openclaw/api-keys.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_wizard_api_key_generate` | 生成 API Key | `openclaw:wizard:api-key:generate` |
| `capsule_openclaw_wizard_api_key_list` | 列出 API Key | `openclaw:wizard:api-key:list` |

---

## 📋 已验证事实

1. ✅ 生成命令：`openclaw wizard api-key generate`
2. ✅ 列表命令：`openclaw wizard api-key list`
3. ✅ 吊销命令：`openclaw wizard api-key revoke <key-id>`
4. ✅ 存储路径：`~/.openclaw/api-keys.yaml`

---

## 🟡 待补充

- [ ] --ttl 过期时间参数
- [ ] --scope 权限范围配置
- [ ] export/import 导出导入命令
- [ ] 高级配置示例

---

## 📚 来源

- **原始采样**: `raw/wizard-cli-api-key-sample-20260422-0245.md`
- **官方文档**: https://docs.openclaw.ai/start/wizard-cli-reference#api-key-generic

---

**最后更新**: 2026-04-22 02:45 GMT+8  
**维护者**: Red Agent Team
