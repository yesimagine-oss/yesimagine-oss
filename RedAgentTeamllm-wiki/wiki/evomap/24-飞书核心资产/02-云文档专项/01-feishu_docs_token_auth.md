---
category: regulatory
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- token
- auth
title: 飞书云文档 Token 认证
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
# Gene: feishu_docs_token_auth

## 摘要

飞书云文档 tenant_access_token 获取与验证

## 策略

1. 调用 GET /open-apis/auth/v3/tenant_access_token/internal
2. 使用 App ID 和 App Secret
3. 验证 token 有效期
4. 缓存 token (2 小时)

## 约束

```json
{
  "token_ttl": "7200s",
  "api_scope": "docx"
}
```

## 验证命令

```bash
pytest tests/test_feishu_docs_token.py
```

## 使用场景

- 云文档 API 调用
- 文档读写权限
- token 管理


## 相關文檔

- [[feishu-evolution-20260413]]
- [[openclaw-docs-deliberation-20260413]]
- [[01-openai-genes]]
