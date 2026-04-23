---
category: regulatory
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- api
- schema
- validate
title: AnyCross API Schema 验证
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
# Gene: anycross_api_schema_validate

## 摘要

AnyCross API 数据格式与字段校验

## 策略

1. 加载 API Schema 定义
2. 验证请求字段完整性
3. 检查数据类型和格式
4. 拒绝不合规请求

## 约束

```json
{
  "schema_version": "1.0",
  "strict_mode": true
}
```

## 验证命令

```bash
node tests/anycross-schema.test.js
```

## 使用场景

- API 调用前验证
- 数据格式检查
- 错误预防


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[asset07_api_batch_optimize]]
