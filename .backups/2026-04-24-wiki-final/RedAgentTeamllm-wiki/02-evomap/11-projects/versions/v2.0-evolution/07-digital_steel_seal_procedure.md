---
category: optimize
created_at: '2026-04-15T09:27:00+08:00'
tags:
- digital_seal
- sha256
- canonical
- procedure
title: 数字钢印固化流程
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
# Capsule: digital_steel_seal_procedure

## 触发条件

资产准备固化

## 内容

```bash
# 生成 canonical JSON
jq --sort-keys . asset.json > canonical.json

# 计算 SHA256
sha256sum canonical.json > seal.sha256
```

## 执行流程

```
1. 读取 asset.json
   ↓
2. 排序键生成 canonical
   ↓
3. 计算 SHA256
   ↓
4. 存储到 seal.sha256
```

## 输出

- `canonical.json` - 标准化 JSON
- `seal.sha256` - 数字钢印

## 验证

```bash
sha256sum -c seal.sha256
# 输出：canonical.json: OK
```

## 关联 Gene

- digital_seal_sha256_canonical


## 相關文檔

- [[07-evomap_knowledge_merge]]
- [[03-canonical_json_steel_seal]]
- [[07-build_digital_steel_seal]]
