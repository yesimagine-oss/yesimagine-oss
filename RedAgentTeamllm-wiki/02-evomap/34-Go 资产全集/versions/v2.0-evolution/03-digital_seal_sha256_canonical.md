---
category: optimize
created_at: '2026-04-15T09:27:00+08:00'
tags:
- sha256
- canonical
- digital_seal
- hash
title: 数字钢印 SHA256 验证
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
# Gene: digital_seal_sha256_canonical

## 摘要

递归 JSON 排序+SHA256 钢印校验

## 策略

1. 使用 jq --sort-keys 生成 canonical JSON
2. 移除所有空白字符
3. 确保 UTF-8 编码一致
4. 计算 SHA256 哈希值
5. 存储哈希到 seal.sha256 文件
6. 验证时重新计算并比对

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
./canonical-hash --verify --input asset.json
```

## 使用场景

- 资产完整性验证
- 防止篡改
- 零漂移保证

## 与现有工具关系

| 现有工具 | 升级内容 |
|---------|---------|
| verify-hash.py | 增加 canonical JSON 标准化 |
| scan-drift.py | 增加数字钢印验证 |


## 相關文檔

- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[03-evomap_drift_pre_scan]]
- [[03-openclaw_config_schema_verify]]
