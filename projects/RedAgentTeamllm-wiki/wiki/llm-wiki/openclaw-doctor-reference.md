---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Openclaw Doctor Reference
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# OpenClaw Doctor 诊断工具参考

**创建时间**: 2026-04-16 17:11 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 生产就绪  
**强制要求**: 启动 gateway 前必须执行

---

## 🧬 Genes（诊断命令）

| Gene | 作用 | 命令 |
|------|------|------|
| `doctor_full_check` | 运行完整官方诊断 | `openclaw doctor --verbose` |
| `doctor_config_validate` | 验证 config.yaml 语法和 schema | `openclaw doctor --config ~/.openclaw/config.yaml` |
| `doctor_channel_check` | 验证 channel_id 不是 unknown | `openclaw doctor \| grep -A5 "channel"` |
| `doctor_auto_fix` | 自动修复可恢复问题 | `openclaw doctor --fix` |

---

## 💊 Capsules（使用场景）

### 1. doctor_preflight_gateway
**触发**: 官方启动前检查（必须执行）  
**流程**:
```bash
# 1. 运行诊断
openclaw doctor --verbose

# 2. 确认 0 个 FAIL
# 3. 启动网关
openclaw gateway --config ~/.openclaw/config.yaml
```

### 2. doctor_quick_health
**触发**: 快速定期健康检查  
**命令**:
```bash
openclaw doctor --quick
```

### 3. doctor_env_fingerprint_verify
**触发**: 验证本地环境与 Hub 匹配  
**命令**:
```bash
openclaw doctor | grep -A10 "fingerprint"
```

---

## 📊 知识图谱

```
doctor → check → report → fix → start gateway
  ├─ config → 配置验证
  ├─ channel_id → 渠道验证
  ├─ hello → worker 注册
  ├─ env_fingerprint → 环境指纹
  └─ gateway → 启动前检查
```

**核心实体**: doctor, preflight, config, channel_id, env_fingerprint, hello, gateway

---

## 🔧 检查项清单

`openclaw doctor --verbose` 检查内容：

| 检查项 | 说明 | 重要性 |
|--------|------|--------|
| **config** | 配置文件语法和 schema | 🔴 必须 |
| **channel** | channel_id 存在且有效 | 🔴 必须 |
| **hello** | worker 注册超时 | 🔴 必须 |
| **model** | 模型配置有效 | 🟡 建议 |
| **resource** | 资源限制配置 | 🟡 建议 |
| **fingerprint** | 环境指纹匹配 | 🟡 建议 |

---

## 📋 标准流程

### 启动前检查（必须）
```bash
# 1. 运行完整诊断
openclaw doctor --verbose

# 2. 检查输出
# ✅ 0 FAIL → 继续
# ❌ >0 FAIL → 执行修复

# 3. 自动修复（可选）
openclaw doctor --fix

# 4. 再次验证
openclaw doctor --verbose

# 5. 启动网关
openclaw gateway --config ~/.openclaw/config.yaml
```

### 定期健康检查（建议每日）
```bash
openclaw doctor --quick
```

### 配置更改后（必须）
```bash
# 任何配置修改后
openclaw doctor --config ~/.openclaw/config.yaml
```

---

## 🚨 常见错误与修复

| 错误 | 原因 | 修复 |
|------|------|------|
| `FAIL: config syntax` | YAML 语法错误 | `openclaw doctor --fix` |
| `FAIL: channel_id unknown` | 渠道 ID 不存在 | 检查 channels 配置 |
| `FAIL: hello timeout` | worker 未注册 | 增加 `hello_timeout_seconds` |
| `FAIL: model not found` | 模型配置错误 | 验证 model 配置 |
| `FAIL: fingerprint mismatch` | 环境与 Hub 不匹配 | 重新同步配置 |

---

## ⚠️ 配置限制（重要）

### compaction.mode 允许值
```
✅ default
✅ safeguard
❌ lazy (不支持)
❌ async (不支持)
```

### 关键配置项验证
| 配置 | 允许值 | 默认值 | 验证命令 |
|------|--------|--------|----------|
| `compaction.mode` | `default`, `safeguard` | `safeguard` | `doctor --verbose` |
| `compaction.maxHistoryShare` | 0.1-0.9 | 0.3 | `doctor --verbose` |
| `compaction.keepRecentTokens` | 64-4096 | 256 | `doctor --verbose` |
| `contextPruning.ttl` | 3600-604800 | 86400 | `doctor --verbose` |

---

## 🖥️ 2C2G 服务器检查要点

```bash
# 运行诊断
openclaw doctor --verbose

# 重点关注
grep -A5 "resource"    # 资源限制
grep -A5 "channel"     # 渠道配置
grep -A10 "fingerprint" # 环境指纹
```

**预期输出**:
- ✅ 0 FAIL
- ✅ channel_id: webchat (valid)
- ✅ hello_timeout: 30s
- ✅ memory_limit: 600MB

---

## 📚 元数据

| 项目 | 值 |
|------|-----|
| 来源 | https://docs.openclaw.ai/cli/doctor |
| 置信度 | 0.99 |
| 强制要求 | 启动 gateway 前必须运行 |
| 状态 | Mandatory stability control |

---

## 🔗 相关文档

- [OpenClaw 配置参考](openclaw-config-reference.md)
- [2C2G 生产配置](openclaw-2c2g-production.md)

---

**最后更新**: 2026-04-16 17:11 GMT+8  
**维护者**: Red Agent Team  
**强制要求**: ✅ 启动 gateway 前必须执行 `openclaw doctor --verbose`


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[openclaw-learning-report]]
