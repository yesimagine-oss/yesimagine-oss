---
category: optimize
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- get
- content
title: 飞书云文档内容获取
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
# Capsule: feishu_docs_get_content

## 触发条件

获取飞书云文档完整内容

## 执行流程

```bash
# 1. 获取 token
GET /open-apis/auth/v3/tenant_access_token/internal

# 2. 获取文档内容
GET /open-apis/docx/v1/documents/{document_id}

# 3. 解析响应
parse_document_content()
```

## 输出

- 文档完整内容
- 块结构列表

## 使用场景

- 文档内容读取
- 批量导出
- 内容分析


## 相關文檔

- [[feishu-evolution-20260413]]
- [[openclaw-docs-deliberation-20260413]]
- [[07-evomap_knowledge_merge]]
