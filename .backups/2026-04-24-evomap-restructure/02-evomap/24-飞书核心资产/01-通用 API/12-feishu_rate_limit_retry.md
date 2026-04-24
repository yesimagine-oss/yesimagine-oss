---
category: optimize
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- rate_limit
- retry
- '429'
title: 飞书限流重试
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
# Capsule: feishu_rate_limit_retry

## 触发条件

收到 429 响应

## 执行流程

```python
# 1. 捕获 429
try:
    call_api()
except 429:
    # 2. 读取 Retry-After
    delay = headers.get('Retry-After', 1)
    
    # 3. 等待并重试
    sleep(delay)
    retry_call()
```

## 输出

- 重试结果
- 最终成功/失败

## 使用场景

- API 限流处理
- 自动重试
- 提高成功率


## 相關文檔

- [[k8s_resource_limit]]
- [[feishu-evolution-20260413]]
- [[asset06_k8s_resource_limit]]
