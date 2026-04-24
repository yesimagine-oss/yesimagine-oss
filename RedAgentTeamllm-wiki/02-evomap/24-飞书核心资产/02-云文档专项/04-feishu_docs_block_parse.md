---
category: optimize
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- block
- parse
title: 飞书文档块结构解析
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
# Gene: feishu_docs_block_parse

## 摘要

飞书云文档块结构解析与操作验证

## 策略

1. 获取文档块列表
2. 解析块类型 (text/image/table 等)
3. 验证块属性和层级
4. 支持块操作 (增删改)

## 约束

```json
{
  "supported_blocks": ["text", "heading", "image", "table", "bullet"],
  "max_depth": 5
}
```

## 验证命令

```bash
node tests/feishu-docs-block.test.js
```

## 使用场景

- 文档结构分析
- 块操作验证
- 内容提取


## 相關文檔

- [[feishu-evolution-20260413]]
- [[openclaw-docs-deliberation-20260413]]
- [[04-evomap_asset_hash_verify]]
