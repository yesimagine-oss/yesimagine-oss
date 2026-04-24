---
category: regulatory
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- webhook
- idempotent
- dedup
title: 飞书 Webhook 去重
type: gene
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
# Gene: feishu_webhook_idempotent

## 摘要

飞书 Webhook 事件幂等性处理

## 策略

1. 提取事件唯一 ID (event_id)
2. 检查是否已处理 (Redis/内存缓存)
3. 未处理则保存并处理
4. 已处理则直接返回成功

## 约束

```json
{
  "cache_ttl": "3600s",
  "storage": "redis"
}
```

## 验证命令

```bash
pytest tests/test_feishu_idempotent.py
```

## 使用场景

- Webhook 事件处理
- 防止重复处理
- 保证幂等性


## 相關文檔

- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[feishu-evolution-20260413]]
- [[03-evomap_drift_pre_scan]]
