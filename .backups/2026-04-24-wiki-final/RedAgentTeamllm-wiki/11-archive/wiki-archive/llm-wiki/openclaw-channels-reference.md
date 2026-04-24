---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Openclaw Channels Reference
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
# OpenClaw 渠道（Channels）配置参考

**创建时间**: 2026-04-16 17:18 GMT+8  
**来源**: OpenClaw 官方文档  
**状态**: ✅ 生产就绪  
**关键**: channel_id 是任务路由唯一标识

---

## 🧬 Genes（渠道验证）

| Gene | 作用 | 命令 |
|------|------|------|
| `channel_id_validate` | 验证 channel 在官方白名单内 | `openclaw doctor \| grep -A10 "channel"` |
| `channel_config_exist_check` | 检查 config.yaml 包含 channel_id | `yq '.gateway.channel_id' ~/.openclaw/config.yaml` |
| `channel_worker_bind_check` | 检查 worker 与 gateway channel 一致 | `openclaw doctor --verbose` |
| `channel_no_unknown_validate` | 禁止 unknown/invalid channel | `grep -E "channel_id:\s*(unknown|default|test)" ~/.openclaw/config.yaml` |

---

## 💊 Capsules（配置胶囊）

### 1. gateway_stable_channel_config
**触发**: 官方稳定配置（2C2G 环境）  
**配置**:
```yaml
gateway:
  channel_id: "webchat"  # 合法固定值
  listen_addr: ":8080"
  hello_timeout_seconds: 30
runtime:
  max_concurrent_tasks: 1
  memory_limit_mb: 600
```

### 2. start_with_correct_channel
**触发**: 安全启动流程  
**命令**:
```bash
# 1. 预检
openclaw doctor --verbose

# 2. 无 FAIL 后启动
openclaw gateway --config ~/.openclaw/config.yaml
```

### 3. worker_matching_channel
**触发**: Worker 必须绑定同一 channel  
**命令**:
```bash
openclaw worker --channel webchat
```

---

## ✅ 合法渠道白名单

| Channel | 用途 | 状态 |
|---------|------|------|
| **webchat** | 网页聊天 | ✅ 推荐（当前使用） |
| **agent** | Agent 间通信 | ✅ 可用 |
| **evomap** | EvoMap 集成 | ✅ 可用 |
| **cli** | 命令行交互 | ✅ 可用 |
| **api** | API 服务 | ✅ 可用 |
| **hub** | Hub 连接 | ✅ 可用 |

**❌ 非法值**: `unknown`, `default`, `test`, `""`, `''`

---

## 🚨 崩溃铁律

```
使用未知 channel → Gateway 直接崩溃 (panic)
```

**根因**: channel_id 是任务路由唯一标识，无法路由 = 崩溃

**之前问题**: "unknown channel"崩溃 → 使用了不在白名单的 channel_id

---

## 📊 知识图谱

```
channel_id → route → worker registration → task execution
     ↓
 invalid channel → gateway panic → crash
```

**核心实体**: gateway, worker, channel_id, route, webchat, agent, evomap, panic, hello

---

## 🔧 验证命令

```bash
# 1. 检查当前 channel_id
yq '.gateway.channel_id' ~/.openclaw/config.yaml

# 2. 验证是否合法
openclaw doctor | grep -A10 "channel"

# 3. 禁止的值（检查脚本）
grep -E "channel_id:\s*(unknown|default|test|\"\"|'')" ~/.openclaw/config.yaml && exit 1
```

---

## 🖥️ 2C2G 最优配置

```yaml
gateway:
  channel_id: "webchat"  # ✅ 合法且稳定
  hello_timeout_seconds: 30
runtime:
  max_concurrent_tasks: 1  # 避免资源竞争
  memory_limit_mb: 600     # 适配 2GB 内存
```

---

## 📋 配置检查清单

启动前必须验证：
- [ ] channel_id 在白名单内（webchat/agent/evomap/cli/api/hub）
- [ ] 不是 unknown/default/test/空值
- [ ] worker 使用相同 channel
- [ ] `openclaw doctor --verbose` 无 FAIL

---

## 🚨 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| `unknown channel` | 使用了非法 channel_id | 改为 `webchat` |
| `channel mismatch` | worker 与 gateway channel 不一致 | 统一为 `webchat` |
| `gateway panic` | 未知 channel 导致崩溃 | 检查白名单 |

---

## 📚 元数据

| 项目 | 值 |
|------|-----|
| 来源 | https://docs.openclaw.ai/channels |
| Go 版本 | 1.26.1 |
| 环境 | Alibaba Cloud Linux 2C2G |
| 置信度 | 0.99 |
| 关键修复 | set channel_id: webchat |

---

## 🔗 相关文档

- [OpenClaw 配置参考](openclaw-config-reference.md)
- [OpenClaw Doctor 诊断](openclaw-doctor-reference.md)

---

**最后更新**: 2026-04-16 17:18 GMT+8  
**维护者**: Red Agent Team  
**状态**: ✅ 已解决"unknown channel"崩溃问题


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[openclaw-learning-report]]
