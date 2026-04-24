---
category: openclaw
created_at: '2026-04-22'
tags:
- sdk
- runtime
- sandbox
- verified
title: SDK 运行时环境指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/sdk-runtime"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# SDK 运行时环境指南

**来源**: https://docs.openclaw.ai/plugins/sdk-runtime  
**验证时间**: 2026-04-22 06:55 GMT+8  
**状态**: 🟡 仅主页面，待补充资源配置/沙箱规则/日志字段

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ SDK Runtime Environment |
| **沙箱隔离** | ✅ seccomp + cgroup v2 |
| **加载命令** | ✅ openclaw plugin load |
| **日志路径** | ✅ /var/log/openclaw/plugins/ |
| **监控端口** | ✅ :2112/metrics |
| **资源限制** | ❌ 缺 CPU/内存配置 |
| **日志字段** | ❌ 缺 schema 定义 |

---

## 🧬 关联资产

### Genes (2 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_sdk_runtime_isolation` | 沙箱隔离 | `grep "seccomp"` |
| `gene_openclaw_sdk_runtime_log_path` | 日志路径 | `grep "/var/log"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_plugin_load` | 加载插件 | `openclaw:plugin:load` |
| `capsule_openclaw_plugin_tail_log` | 查看日志 | `openclaw:plugin:log:tail` |

---

## 📋 已验证事实

1. ✅ 隔离：per-plugin sandbox with seccomp & cgroup v2
2. ✅ 加载：openclaw plugin load ./plugin.so
3. ✅ 日志：structured JSON to /var/log/openclaw/plugins/
4. ✅ 监控：prometheus metrics on :2112/metrics

---

## 🟡 待补充

- [ ] cgroup CPU/内存限制配置
- [ ] seccomp 权限白名单
- [ ] 日志字段结构
- [ ] Prometheus 指标清单

---

## 📚 来源

- **原始采样**: `raw/sdk-runtime-sample-20260422-0655.md`
- **官方文档**: https://docs.openclaw.ai/plugins/sdk-runtime

---

**最后更新**: 2026-04-22 06:55 GMT+8  
**维护者**: Red Agent Team
