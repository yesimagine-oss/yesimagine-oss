---
category: regulatory
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- auth
- verify
- credential
title: AnyCross 认证验证
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
# Gene: anycross_auth_verify

## 摘要

验证 AnyCross 跨系统授权合法性

## 策略

1. 获取连接器凭证 (credential)
2. 验证凭证有效期
3. 检查授权范围 (scope)
4. 拒绝未授权请求

## 约束

```json
{
  "credential_ttl": "3600s",
  "required_scopes": ["connector:read", "connector:write"]
}
```

## 验证命令

```bash
pytest tests/test_anycross_auth.py
```

## 使用场景

- 连接器调用前验证
- 跨系统授权
- 凭证管理


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[04-evomap_asset_hash_verify]]
