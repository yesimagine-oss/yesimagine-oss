---
category: openclaw
created_at: '2026-04-22'
tags:
- start
- getting-started
- verified
title: OpenClaw 快速入门指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/start/openclaw"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# OpenClaw 快速入门指南

**来源**: https://docs.openclaw.ai/start/openclaw  
**验证时间**: 2026-04-22 03:05 GMT+8  
**状态**: 🟡 仅主页面，待补充重启命令与完整配置示例

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Getting Started with OpenClaw |
| **启动命令** | ✅ `openclaw start` |
| **停止命令** | ✅ `openclaw stop` |
| **状态命令** | ✅ `openclaw status` |
| **主配置路径** | ✅ `/etc/openclaw/config.yaml` |
| **重启命令** | ❌ 缺 `openclaw restart` |
| **日志查看** | ❌ 缺 logs 命令 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_start_title` | 入门指南标题 | `grep "Getting Started with OpenClaw"` |
| `gene_openclaw_start_cmd` | 启动命令 | `grep "openclaw start"` |
| `gene_openclaw_main_config_path` | 主配置路径 | `grep "/etc/openclaw/config.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_start_service` | 启动服务 | `openclaw:start` |
| `capsule_openclaw_check_status` | 检查状态 | `openclaw:status` |

---

## 📋 已验证事实

1. ✅ 启动命令：`openclaw start`
2. ✅ 停止命令：`openclaw stop`
3. ✅ 状态检查：`openclaw status`
4. ✅ 主配置路径：`/etc/openclaw/config.yaml`

---

## 🟡 待补充

- [ ] `openclaw restart` 重启命令
- [ ] 日志查看命令
- [ ] config.yaml 完整配置示例
- [ ] 初始化向导命令

---

## 📚 来源

- **原始采样**: `raw/getting-started-sample-20260422-0305.md`
- **官方文档**: https://docs.openclaw.ai/start/openclaw

---

**最后更新**: 2026-04-22 03:05 GMT+8  
**维护者**: Red Agent Team
