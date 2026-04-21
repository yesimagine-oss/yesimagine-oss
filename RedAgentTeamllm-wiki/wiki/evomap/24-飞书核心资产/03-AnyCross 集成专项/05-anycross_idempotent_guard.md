---
category: regulatory
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- idempotent
- guard
- dedup
title: AnyCross 幂等性防护
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
# Gene: anycross_idempotent_guard

## 摘要

跨系统流程幂等性防重复执行

## 策略

1. 生成流程唯一 ID
2. 检查是否已执行 (Redis)
3. 未执行则保存并执行
4. 已执行则返回缓存结果

## 约束

```json
{
  "cache_ttl": "7200s",
  "storage": "redis",
  "key_prefix": "anycross:idempotent:"
}
```

## 验证命令

```bash
pytest tests/test_anycross_idempotent.py
```

## 使用场景

- 跨系统流程去重
- 防止重复执行
- 保证幂等性


## 相關文檔

- [[05-evomap_asset_safe_submit]]
- [[05-openclaw_gateway_forward]]
- [[05-corona10-genes]]
