---
category: optimize
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- worker
- register
- hello
title: OpenClaw Worker 注册
type: capsule
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
# Capsule: openclaw_worker_register

## 触发条件

节点启动 / 重连

## 执行流程

```bash
# 1. 注册 Worker
POST /v1/worker/register
{
  "worker_id": "...",
  "capabilities": [...]
}

# 2. Hello 握手
await hello_handshake()

# 3. 确认渠道路由
confirm_channel_routing()
```

## 输出

- 注册成功确认
- Worker ID
- 可用渠道列表

## 使用场景

- Worker 启动
- 重连恢复
- 能力注册


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[06-evomap_node_re_register]]
