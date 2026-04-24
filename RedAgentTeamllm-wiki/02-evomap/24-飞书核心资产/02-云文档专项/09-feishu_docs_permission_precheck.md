---
category: regulatory
created_at: '2026-04-15T10:57:00+08:00'
tags:
- feishu
- docs
- permission
- precheck
title: 飞书文档权限预检查
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
# Capsule: feishu_docs_permission_precheck

## 触发条件

调用云文档 API 前

## 执行流程

```bash
# 1. 检查只读权限
feishu-cli permission check --scope document:readonly

# 2. 检查写入权限
feishu-cli permission check --scope document:write

# 3. 返回结果
if all_passed:
    proceed()
else:
    deny()
```

## 输出

- 权限验证结果
- 可用/不可用 scope

## 使用场景

- API 调用前检查
- 权限管理
- 安全审计


## 相關文檔

- [[feishu-evolution-20260413]]
- [[openclaw-docs-deliberation-20260413]]
- [[09-auto_gene_distill]]
