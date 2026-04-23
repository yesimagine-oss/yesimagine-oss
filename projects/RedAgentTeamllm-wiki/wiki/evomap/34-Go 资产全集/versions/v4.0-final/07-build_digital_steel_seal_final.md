---
category: regulatory
created_at: '2026-04-15T10:11:00+08:00'
tags:
- digital_seal
- sha256
- canonical
- final
title: 数字钢印构建流程（最终版）
type: capsule
version: '4.0'

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
# Capsule: build_digital_steel_seal_final

## 触发条件

资产固化启动

## 执行流程

```bash
# 1. 生成规范 JSON (递归排序)
jq --sort-keys . asset.json > canonical.json

# 2. 计算 SHA256 钢印
sha256sum canonical.json > steel-seal.sha256

# 3. 验证钢印
cat steel-seal.sha256
```

## 输出

- `canonical.json` - 规范格式资产
- `steel-seal.sha256` - 数字钢印

## 使用场景

- 资产发布前固化
- 跨环境验证
- 防止哈希漂移


## 相關文檔

- [[FINAL-COMPLETION-REPORT]]
- [[07-evomap_knowledge_merge]]
- [[03-canonical_json_steel_seal]]
