---
category: optimize
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- rate_limit
- '429'
- retry
title: 飞书限流处理
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
# Gene: feishu_rate_limit_handle

## 摘要

飞书 API 429 限流自动重试策略

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
node tests/feishu-rate-limit.test.js
```

## 使用场景

- API 调用限流
- 自动重试
- 提高成功率


## 相關文檔

- [[k8s_resource_limit]]
- [[feishu-evolution-20260413]]
- [[asset06_k8s_resource_limit]]
