---
category: regulatory
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- api
- auth
- token
title: 飞书 API 认证
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
# Gene: feishu_api_auth

## 摘要

飞书 tenant_access_token 获取与验证

## 策略

1. 调用 GET /open-apis/auth/v3/tenant_access_token/internal
2. 使用 App ID 和 App Secret
3. 缓存 token (有效期 2 小时)
4. 自动刷新过期 token

## 约束

```json
{
  "token_ttl": "7200s",
  "refresh_before": "300s"
}
```

## 验证命令

```bash
node tests/feishu-token-test.js
```

## 使用场景

- API 调用前认证
- 多租户应用
- token 管理


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[feishu-evolution-20260413]]
