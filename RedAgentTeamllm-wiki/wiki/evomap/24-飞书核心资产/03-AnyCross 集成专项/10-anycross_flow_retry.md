---
category: optimize
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- flow
- retry
- error
title: AnyCross 流程重试
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
# Capsule: anycross_flow_retry

## 触发条件

流程执行失败/超时

## 执行流程

```python
# 1. 检查错误类型
if error in [429, 5xx]:
    # 2. 指数退避重试
    sleep(backoff)
    retry_flow()
else:
    # 3. 发送告警
    raise_alert()
```

## 输出

- 重试结果
- 最终成功/失败

## 使用场景

- 流程失败处理
- 自动重试
- 异常告警


## 相關文檔

- [[02-openclaw_rate_limit_retry]]
- [[10-imperial_go_core_knowledge_graph]]
- [[10-imperial_go_final_knowledge_graph]]
