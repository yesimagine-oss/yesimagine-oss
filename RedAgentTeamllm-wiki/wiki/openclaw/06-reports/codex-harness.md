---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- codex
- security
- verified
title: Codex-Harness 沙箱插件指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/codex-harness"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Codex-Harness 沙箱插件指南

**来源**: https://docs.openclaw.ai/plugins/codex-harness  
**验证时间**: 2026-04-22 05:05 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/调用方式/安全策略

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Codex Harness Plugin |
| **核心用途** | ✅ secure code execution & sandboxed |
| **安装命令** | ✅ openclaw plugin install codex-harness |
| **配置路径** | ✅ /etc/openclaw/plugins/codex-harness.yaml |
| **核心能力** | ✅ isolate, timeout, resource-limit, log-capture |
| **完整配置** | ❌ 缺 YAML 示例 |
| **调用方式** | ❌ 缺执行接口 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_codex_harness_title` | 插件标题 | `grep "Codex Harness Plugin"` |
| `gene_openclaw_codex_install_cmd` | 安装命令 | `grep "openclaw plugin install codex-harness"` |
| `gene_openclaw_codex_config_path` | 配置路径 | `grep "/etc/openclaw/plugins/codex-harness.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_codex_harness` | 安装沙箱插件 | `openclaw:plugin:install:codex-harness` |
| `capsule_openclaw_edit_codex_config` | 编辑配置 | `openclaw:plugin:codex:config:edit` |

---

## 📋 已验证事实

1. ✅ 用途：secure code execution & sandboxed agent runtime
2. ✅ 安装：openclaw plugin install codex-harness
3. ✅ 配置：/etc/openclaw/plugins/codex-harness.yaml
4. ✅ 能力：isolate, timeout, resource-limit, log-capture

---

## 🟡 待补充

- [ ] 完整 YAML 配置示例
- [ ] 运行时调用接口
- [ ] 资源限制默认值 (CPU/内存)
- [ ] 安全策略/权限白名单

---

## 📚 来源

- **原始采样**: `raw/codex-harness-sample-20260422-0505.md`
- **官方文档**: https://docs.openclaw.ai/plugins/codex-harness

---

**最后更新**: 2026-04-22 05:05 GMT+8  
**维护者**: Red Agent Team
