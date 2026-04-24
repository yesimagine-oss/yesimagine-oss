---
category: optimize
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- rate_limit
- retry
title: 飞书云文档频控重试
type: gene
version: '2.0'

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
# Gene: feishu_docs_rate_limit_retry

## 摘要

飞书云文档 API 429 频控自动重试策略

## 策略

1. 捕获 429 响应
2. 读取 Retry-After 头
3. 等待指定时间后重试
4. 最多重试 3 次

## 约束

```json
{
  "max_retries": 3,
  "base_delay": "1s"
}
```

## 验证命令

```bash
pytest tests/test_feishu_docs_ratelimit.py
```

## 使用场景

- 文档 API 限流
- 自动重试
- 提高成功率


## 相關文檔

- [[k8s_resource_limit]]
- [[feishu-evolution-20260413]]
- [[openclaw-docs-deliberation-20260413]]
