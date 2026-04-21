---
category: optimize
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- bot
- message
- send
title: 飞书机器人消息发送
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
# Capsule: feishu_bot_message_send

## 触发条件

需要发送飞书消息

## 执行流程

```bash
# 1. 获取 token
GET /open-apis/auth/v3/tenant_access_token/internal

# 2. 发送消息
POST /open-apis/im/v1/messages
{
  "receive_id": "ou_xxx",
  "msg_type": "interactive",
  "content": {...}
}
```

## 输出

- 消息发送成功确认
- message_id

## 使用场景

- 机器人通知
- 消息推送
- 交互式卡片


## 相關文檔

- [[feishu-evolution-20260413]]
- [[08-hunter_deferred_claim]]
- [[08-hunter_deferred_claim_final]]
