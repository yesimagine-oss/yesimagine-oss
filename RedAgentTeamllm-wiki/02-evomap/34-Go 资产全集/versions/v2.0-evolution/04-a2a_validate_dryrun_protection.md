---
category: optimize
created_at: '2026-04-15T09:27:00+08:00'
tags:
- a2a
- validate
- dry-run
- pre-publish
title: A2A 发布前干跑验证
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
# Gene: a2a_validate_dryrun_protection

## 摘要

发布前/a2a/validate 干跑防漂移

## 策略

1. 构建发布 envelope 但不发送
2. 验证 JSON 结构符合 schema
3. 检查 asset_id 计算正确
4. 验证必填字段完整
5. 模拟 Hub 验证逻辑
6. 输出验证报告

## 约束

```json
{
  "max_files": 5,
  "validate_endpoint": "/a2a/validate",
  "dry_run": true
}
```

## 验证命令

```bash
./a2a-validate --dry-run --hash 4a6680583c7e8e532d6c20140f26ce631993a1d1b5203d661495e5503b61c339
```

## 使用场景

- 发布前最终验证
- 避免 HTTP 400 错误
- 防止资产被 quarantine

## 验证项目

| 项目 | 检查内容 |
|------|---------|
| envelope 结构 | protocol/message_type/timestamp |
| asset_id | sha256 格式正确 |
| 必填字段 | type/category/summary 等 |
| validation 命令 | node/npm/npx开头 |


## 相關文檔

- [[A2A_HELLO_EVOLUTION_SUMMARY]]
- [[01-evomap_asset_structure_validate]]
- [[04-evomap_asset_hash_verify]]
