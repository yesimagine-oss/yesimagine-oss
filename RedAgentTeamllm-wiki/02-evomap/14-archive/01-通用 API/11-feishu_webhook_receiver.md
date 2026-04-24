---
category: optimize
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- webhook
- receiver
- event
title: 飞书 Webhook 接收器
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
# Capsule: feishu_webhook_receiver

## 触发条件

Webhook 事件到达

## 执行流程

```python
# 1. 验证签名
verify_signature(payload, headers)

# 2. 保存事件 (去重)
save_event_unique(event_id)

# 3. 分发处理
dispatch_event(event_type)
```

## 输出

- 事件接收确认
- HTTP 200 响应

## 使用场景

- Webhook 接收
- 事件分发
- 异步处理

## 依赖

- feishu_signature_verify
- feishu_webhook_idempotent


## 相關文檔

- [[feishu-evolution-20260413]]
- [[11-go_asset_learning_report]]
- [[11-go_asset_final_learning_report]]
