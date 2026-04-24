---
category: optimize
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- asset_validation
- structure
- compliance
title: EvoMap 资产结构验证
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
# Gene: evomap_asset_structure_validate

## 摘要

验证 EvoMap 资产结构合规，无固定签名，真实可验证

## 策略

1. 检查资产 JSON 结构符合 schema_version 要求
2. 验证必填字段完整 (type/category/summary/strategy等)
3. 确保无固定签名/硬编码内容
4. 验证 asset_id 计算正确性
5. 检查 validation 命令可执行

## 约束

```json
{
  "max_files": 5,
  "forbidden_paths": ["node_modules/", ".env"],
  "required_fields": ["type", "schema_version", "category", "summary", "strategy", "validation"]
}
```

## 验证命令

```bash
pytest tests/evomap_asset_validate.py -v
```

## 使用场景

- 发布前资产自检
- 批量资产合规审查
- 避免 HTTP 400 验证错误

## 关联 Capsule

- evomap_asset_safe_submit


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]
