---
category: regulatory
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- permission
- check
- scope
title: 飞书应用权限检查
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
# Capsule: feishu_app_permission_check

## 触发条件

调用飞书 API 前

## 执行流程

```bash
# 1. 检查权限列表
feishu-cli permission list

# 2. 验证所需 scope
feishu-cli permission check --scope document:readonly
feishu-cli permission check --scope document:write
```

## 输出

- 权限验证结果
- 可用/不可用 scope 列表

## 使用场景

- API 调用前检查
- 权限管理
- 安全审计


## 相關文檔

- [[feishu-evolution-20260413]]
- [[02-evomap_node_health_check]]
- [[01-openclaw_channel_id_check]]
