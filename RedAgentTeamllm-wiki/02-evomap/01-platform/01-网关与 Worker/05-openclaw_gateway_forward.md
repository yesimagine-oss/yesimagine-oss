---
category: optimize
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- gateway
- forward
- message
title: OpenClaw 网关转发
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
# Capsule: openclaw_gateway_forward

## 触发条件

外部消息进入网关

## 执行流程

```python
# 1. 验证签名
verify_signature(headers, payload)

# 2. 路由到渠道
route_to_channel(channel_id)

# 3. 转发到 Worker
forward_to_worker()
```

## 输出

- 消息转发结果
- Worker 处理状态

## 使用场景

- 消息接收
- 渠道路由
- Worker 分发


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[05-evomap_asset_safe_submit]]
