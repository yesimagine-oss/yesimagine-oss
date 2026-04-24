---
category: regulatory
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- webhook
- signature
title: 飞书文档事件签名校验
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
# Gene: feishu_webhook_signature_validate

## 摘要

飞书云文档事件签名校验

## 策略

1. 从 X-Feishu-Signature 头提取签名
2. 使用 HMAC-SHA256 算法验证
3. 比对计算签名与请求签名
4. 拒绝未通过签名的请求

## 约束

```json
{
  "algorithm": "HMAC-SHA256",
  "header": "X-Feishu-Signature"
}
```

## 验证命令

```bash
pytest tests/test_feishu_webhook_signature.py
```

## 使用场景

- 文档变更事件验证
- Webhook 安全
- 防止伪造


## 相關文檔

- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[feishu-evolution-20260413]]
- [[03-evomap_drift_pre_scan]]
