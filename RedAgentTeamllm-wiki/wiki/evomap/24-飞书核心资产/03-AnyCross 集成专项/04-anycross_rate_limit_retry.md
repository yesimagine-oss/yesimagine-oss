---
category: optimize
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- rate_limit
- retry
- '429'
title: AnyCross 限流重试
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
# Gene: anycross_rate_limit_retry

## 摘要

AnyCross API 429 限流自动重试与降级策略

## 策略

1. 捕获 429 响应
2. 读取 Retry-After 头
3. 指数退避重试 (1s, 2s, 4s)
4. 超过阈值则降级处理

## 约束

```json
{
  "max_retries": 3,
  "backoff_multiplier": 2,
  "fallback": "queue"
}
```

## 验证命令

```bash
node tests/anycross-ratelimit.test.js
```

## 使用场景

- API 限流处理
- 自动重试
- 降级策略


## 相關文檔

- [[k8s_resource_limit]]
- [[asset06_k8s_resource_limit]]
- [[04-evomap_asset_hash_verify]]
