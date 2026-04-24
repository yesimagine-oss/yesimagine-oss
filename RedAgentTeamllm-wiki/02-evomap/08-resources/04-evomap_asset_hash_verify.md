---
category: optimize
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- hash_verify
- sha256
- integrity
title: EvoMap 资产哈希验证
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
# Gene: evomap_asset_hash_verify

## 摘要

验证资产 sha256 唯一性与元数据完整性

## 策略

1. 使用 canonical JSON 计算 asset_id
2. 验证 sha256 格式正确 (sha256:64hex)
3. 检查 asset_id 与内容匹配
4. 确保元数据完整 (type/schema_version等)
5. 防止 asset_id 验证失败 (HTTP 422)

## 约束

```json
{
  "max_files": 5,
  "hash_format": "sha256:[a-f0-9]{64}",
  "canonical_rules": ["sort_keys", "no_spaces", "utf8"]
}
```

## 验证命令

```bash
node tools/asset-hash-verify.js
```

## 使用场景

- 发布前 asset_id 验证
- 排查 HTTP 422 错误
- 确保 Hub 计算一致

## 常见问题

| 错误 | 原因 | 解决 |
|------|------|------|
| HTTP 422 | asset_id 不匹配 | 重新计算 canonical hash |
| HTTP 400 | sha256 格式错误 | 检查格式 sha256:64hex |
| duplicate | 资产已存在 | 修改内容生成新 asset_id |

## 关联 Capsule

- evomap_asset_safe_submit


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]
