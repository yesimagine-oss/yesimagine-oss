---
category: optimize
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- block
- operate
title: 飞书文档块操作
type: capsule
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
# Capsule: feishu_docs_block_operate

## 触发条件

新增/修改/删除文档块

## 执行流程

```bash
# 1. 构造操作请求
POST /open-apis/docx/v1/documents/{doc_id}/blocks/{block_id}/operations
{
  "operations": [
    {"type": "insert", "block": {...}},
    {"type": "update", "block_id": "...", "fields": {...}}
  ]
}

# 2. 执行操作
execute_operations()

# 3. 验证结果
verify_result()
```

## 输出

- 操作结果
- 更新后的块列表

## 使用场景

- 文档内容编辑
- 批量更新
- 自动化文档


## 相關文檔

- [[feishu-evolution-20260413]]
- [[openclaw-docs-deliberation-20260413]]
- [[10-imperial_go_core_knowledge_graph]]
