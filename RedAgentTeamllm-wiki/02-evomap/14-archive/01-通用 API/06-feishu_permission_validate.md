---
category: regulatory
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- permission
- scope
- validate
title: 飞书权限验证
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
# Gene: feishu_permission_validate

## 摘要

飞书应用权限范围合法性验证

## 策略

1. 获取应用权限列表
2. 验证所需 scope 是否存在
3. 检查权限有效期
4. 拒绝越权操作

## 约束

```json
{
  "required_scopes": ["im:message", "contact:readonly"]
}
```

## 验证命令

```bash
pytest tests/test_feishu_permission.py
```

## 使用场景

- API 调用前检查
- 权限管理
- 安全审计


## 相關文檔

- [[feishu-evolution-20260413]]
- [[06-evomap_node_re_register]]
- [[01-evomap_asset_structure_validate]]
