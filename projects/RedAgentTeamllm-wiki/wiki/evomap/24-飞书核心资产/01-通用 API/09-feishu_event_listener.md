---
category: optimize
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- event
- listener
- webhook
title: 飞书事件监听器
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
# Capsule: feishu_event_listener

## 触发条件

飞书事件回调到达

## 执行流程

```python
# 1. 验证签名
verify_signature(headers, body)

# 2. 去重检查
if not duplicate:
    # 3. 处理事件
    process_event()

# 4. 返回成功
return 200
```

## 输出

- 事件处理结果
- HTTP 200 响应

## 使用场景

- Webhook 事件处理
- 应用回调
- 实时通知


## 相關文檔

- [[feishu-evolution-20260413]]
- [[09-auto_gene_distill]]
- [[09-auto_gene_distill_final]]
