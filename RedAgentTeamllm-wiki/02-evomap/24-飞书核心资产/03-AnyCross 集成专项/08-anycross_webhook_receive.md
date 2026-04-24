---
category: optimize
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- webhook
- receive
- event
title: AnyCross Webhook 接收
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
# Capsule: anycross_webhook_receive

## 触发条件

跨系统事件回调到达

## 执行流程

```python
# 1. 验证签名
verify_signature(headers, body)

# 2. 去重检查
deduplicate_by_event_id()

# 3. 分发到流程
dispatch_to_flow()
```

## 输出

- 事件处理结果
- HTTP 200 响应

## 使用场景

- Webhook 接收
- 事件分发
- 跨系统通知


## 相關文檔

- [[08-hunter_deferred_claim]]
- [[08-hunter_deferred_claim_final]]
- [[08-hunter_deferred_claim_prime]]
