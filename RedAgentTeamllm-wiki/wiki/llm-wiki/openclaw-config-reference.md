---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Openclaw Config Reference
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
# OpenClaw 配置参考手册

**创建时间**: 2026-04-16 17:05 GMT+8  
**来源**: 用户提供的基因/胶囊/知识图谱  
**状态**: ✅ 生产就绪

---

## 🧬 Genes（核心验证）

| Gene | 作用 | 命令 |
|------|------|------|
| `openclaw_channel_validation` | 验证渠道 ID 存在且有效 | `openclaw gateway --config-test` |
| `openclaw_worker_hello_check` | 确保 worker 在超时内发送 hello | `openclaw worker --debug` |
| `openclaw_resource_limit_validate` | 验证内存/CPU 限制已应用 | `cgget -r memory.limit_in_bytes openclaw` |
| `openclaw_config_parse_check` | 验证 YAML 配置语法 | `yq ~/.openclaw/config.yaml` |

---

## 💊 Capsules（配置胶囊）

### 1. openclaw_gateway_start
**触发**: 官方稳定网关启动  
**命令**:
```bash
openclaw gateway --config ~/.openclaw/config.yaml
```

### 2. openclaw_2c2g_production_config
**触发**: 小服务器加固（2C2G）  
**配置**:
```yaml
model:
  default: gemini-1.5-flash
  max_context_tokens: 8192
runtime:
  max_concurrent_tasks: 1
  memory_limit_mb: 600
  cpu_share: 50
gateway:
  channel_id: "webchat"
  hello_timeout_seconds: 30
```

### 3. openclaw_resource_apply
**触发**: 对运行中的 PID 应用 cgroup 限制  
**命令**:
```bash
sudo cgset -r memory.limit_in_bytes=600M openclaw
sudo cgclassify -g memory:/openclaw <pid>
renice 19 -p <pid>
```

---

## 📊 知识图谱

```
OpenClaw
  ├─ gateway → worker hello → 任务路由
  ├─ config.yaml → 渠道验证 → channel_id 必须有效
  ├─ 模型推理 → 资源限制
  └─ cgroup → 内存/CPU 限制
```

**核心实体**: OpenClaw, gateway, worker, channel_id, hello, config.yaml, cgroup, gemini

---

## ⚠️ 配置限制（重要）

### compaction.mode 允许值
```
✅ default
✅ safeguard
❌ lazy (不支持)
```

### 关键配置项
| 配置 | 允许值 | 默认值 |
|------|--------|--------|
| `compaction.mode` | `default`, `safeguard` | `safeguard` |
| `compaction.maxHistoryShare` | 0.1-0.9 | 0.3 |
| `compaction.keepRecentTokens` | 64-4096 | 256 |
| `contextPruning.ttl` | 3600-604800 | 86400 |

---

## 🖥️ 2C2G 服务器优化配置

| 资源 | 限制 | 说明 |
|------|------|------|
| **内存** | 600MB | cgroup 硬限制 |
| **CPU** | renice 19 | 低优先级 |
| **并发任务** | 1 | 避免资源竞争 |
| **上下文 tokens** | 8192 | 模型级别限制 |
| **hello 超时** | 30s | worker 注册超时 |

---

## 🔧 常用命令

```bash
# 配置测试
openclaw gateway --config-test

# 详细诊断
openclaw doctor --verbose

# 查看帮助
openclaw help

# 重启网关
openclaw gateway restart

# 检查状态
openclaw status

# 验证配置语法
yq ~/.openclaw/config.yaml

# 应用资源限制
sudo cgset -r memory.limit_in_bytes=600M openclaw
sudo cgclassify -g memory:/openclaw <pid>
renice 19 -p <pid>
```

---

## 📋 配置验证清单

执行配置更改前：
- [ ] `openclaw doctor --verbose` 检查支持项
- [ ] 备份配置文件 `cp config.json config.json.bak`
- [ ] 验证 channel_id 存在
- [ ] 验证 compaction.mode 是 `default` 或 `safeguard`

执行配置更改后：
- [ ] `openclaw gateway restart` 重启
- [ ] `openclaw status` 验证状态
- [ ] 观察 worker hello 是否正常

---

## 🚨 常见错误与修复

| 错误 | 原因 | 修复 |
|------|------|------|
| `compaction.mode: Invalid input` | 使用了不支持的模式 | 改为 `default` 或 `safeguard` |
| `channel_id not found` | 渠道 ID 不存在 | 检查 channels 配置 |
| `worker hello timeout` | worker 未注册 | 检查 `hello_timeout_seconds` |
| `memory limit exceeded` | 超出 cgroup 限制 | 调整 `memory_limit_mb` |

---

## 📚 元数据

| 项目 | 值 |
|------|-----|
| 来源 | https://docs.openclaw.ai/help |
| 环境 | Alibaba Cloud Linux 2C2G |
| Go 版本 | 1.26.1 |
| 置信度 | 0.99 |
| 状态 | Stable, production-ready |

---

**最后更新**: 2026-04-16 17:05 GMT+8  
**维护者**: Red Agent Team


## 相關文檔

- [[serper-api-config]]
- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
