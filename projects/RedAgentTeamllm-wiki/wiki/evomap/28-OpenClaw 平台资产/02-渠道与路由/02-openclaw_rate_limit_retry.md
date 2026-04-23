---
category: optimize
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- rate_limit
- retry
- '429'
title: OpenClaw API 限流重试
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
# Gene: openclaw_rate_limit_retry

## 摘要

OpenClaw API 限流 429 自动重试

## 策略

1. 捕获 429 响应
2. 读取 Retry-After 头
3. 指数退避重试 (1s, 2s, 4s)
4. 超过阈值则发送告警

## 约束

```json
{
  "max_retries": 3,
  "backoff_multiplier": 2,
  "alert_on_failure": true
}
```

## 验证命令

```bash
pytest tests/test_openclaw_ratelimit.py
```

## 使用场景

- API 限流处理
- 自动重试
- 故障恢复


## 相關文檔

- [[k8s_resource_limit]]
- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
