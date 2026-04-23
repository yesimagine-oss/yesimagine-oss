---
category: optimize
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- connector
- sync
- data
title: AnyCross 连接器同步
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
# Capsule: anycross_connector_sync

## 触发条件

同步第三方系统数据至飞书

## 执行流程

```bash
# 1. 获取连接器信息
GET /open-apis/anycross/v1/connectors/{connector_id}

# 2. 同步数据
POST /open-apis/anycross/v1/data/sync
{
  "connector_id": "...",
  "data": {...}
}

# 3. 验证结果
verify_sync_result()
```

## 输出

- 同步结果
- 数据状态

## 使用场景

- 数据同步
- 第三方集成
- 跨系统数据流转


## 相關文檔

- [[09-auto_gene_distill]]
- [[09-auto_gene_distill_final]]
- [[09-auto_gene_distill_prime]]
