---
category: regulatory
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- permission
- scope
title: 飞书云文档权限验证
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
# Gene: feishu_docs_permission_verify

## 摘要

验证云文档读写/授权范围合法性

## 策略

1. 检查 document:readonly scope
2. 检查 document:write scope
3. 验证文档访问权限
4. 拒绝越权操作

## 约束

```json
{
  "required_scopes": ["docx:document", "docx:document:readonly"]
}
```

## 验证命令

```bash
node tests/feishu-docs-permission.test.js
```

## 使用场景

- 文档访问前检查
- 权限管理
- 安全审计


## 相關文檔

- [[feishu-evolution-20260413]]
- [[openclaw-docs-deliberation-20260413]]
- [[02-openai-capsules]]
