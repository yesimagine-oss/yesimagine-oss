---
category: regulatory
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- webhook
- signature
- check
title: AnyCross Webhook 签名校验
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
# Gene: anycross_webhook_signature_check

## 摘要

AnyCross 事件回调签名校验

## 策略

1. 从请求头提取签名
2. 使用 HMAC-SHA256 算法验证
3. 比对计算签名与请求签名
4. 拒绝未通过签名的请求

## 约束

```json
{
  "algorithm": "HMAC-SHA256",
  "header": "X-AnyCross-Signature"
}
```

## 验证命令

```bash
pytest tests/test_anycross_webhook.py
```

## 使用场景

- Webhook 事件验证
- 防止伪造请求
- 跨系统安全


## 相關文檔

- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[03-evomap_drift_pre_scan]]
- [[02-evomap_node_health_check]]
