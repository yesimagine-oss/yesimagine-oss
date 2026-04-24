---
category: regulatory
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- gateway
- signature
- validate
title: OpenClaw 网关签名校验
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
# Gene: openclaw_gateway_signature_validate

## 摘要

OpenClaw 网关请求签名校验

## 策略

1. 从 X-OpenClaw-Signature 头提取签名
2. 使用 HMAC-SHA256 算法验证
3. 比对计算签名与请求签名
4. 拒绝未通过签名的请求

## 约束

```json
{
  "algorithm": "HMAC-SHA256",
  "header": "X-OpenClaw-Signature"
}
```

## 验证命令

```bash
node tests/openclaw-gateway-signature.test.js
```

## 使用场景

- 网关请求验证
- 防止伪造请求
- 平台安全


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[02-openai-capsules]]
