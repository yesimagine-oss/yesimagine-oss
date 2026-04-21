---
category: regulatory
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- signature
- verify
- security
title: 飞书签名验证
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
# Gene: feishu_signature_verify

## 摘要

飞书开放平台请求签名验证

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
pytest tests/test_feishu_signature.py
```

## 使用场景

- Webhook 请求验证
- API 调用安全
- 防止伪造请求


## 相關文檔

- [[feishu-evolution-20260413]]
- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
