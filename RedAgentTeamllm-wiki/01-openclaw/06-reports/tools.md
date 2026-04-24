---
category: openclaw
created_at: '2026-04-22'
tags:
- tools
- utilities
- verified
title: 内置工具与实用程序指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 内置工具与实用程序指南

**来源**: https://docs.openclaw.ai/tools  
**验证时间**: 2026-04-22 04:25 GMT+8  
**状态**: 🟡 仅主页面，待补充详细参数与高级用法

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ OpenClaw Tools & Utilities |
| **check 工具** | ✅ config & health validation |
| **secret 工具** | ✅ secure secret generation |
| **lint 工具** | ✅ configuration linting |
| **export 工具** | ✅ config & state export |
| **详细参数** | ❌ 缺 --help / 示例 |
| **import 工具** | ❌ 缺导入功能 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_tools_title` | 工具文档标题 | `grep "OpenClaw Tools & Utilities"` |
| `gene_openclaw_tool_check` | check 工具 | `grep "openclaw check"` |
| `gene_openclaw_tool_secret` | secret 工具 | `grep "openclaw secret"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_check_config` | 检查配置 | `openclaw:tools:check` |
| `capsule_openclaw_lint_config` | 配置语法检查 | `openclaw:tools:lint` |

---

## 📋 已验证事实

1. ✅ check: 配置与健康检查
2. ✅ secret: 安全生成密钥
3. ✅ lint: 配置语法检查
4. ✅ export: 导出配置与状态

---

## 🟡 待补充

- [ ] 各工具详细命令参数
- [ ] import 导入工具
- [ ] 日志查看工具
- [ ] 权限检查工具

---

## 📚 来源

- **原始采样**: `raw/tools-sample-20260422-0425.md`
- **官方文档**: https://docs.openclaw.ai/tools

---

**最后更新**: 2026-04-22 04:25 GMT+8  
**维护者**: Red Agent Team
