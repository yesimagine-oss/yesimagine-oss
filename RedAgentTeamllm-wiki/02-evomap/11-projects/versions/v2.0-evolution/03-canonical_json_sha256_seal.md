---
category: regulatory
created_at: '2026-04-15T09:55:00+08:00'
tags:
- sha256
- canonical
- json
- digital_seal
- hash
title: Canonical JSON SHA256 数字钢印
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
# Gene: canonical_json_sha256_seal

## 摘要

递归排序 JSON 并生成 SHA256 数字钢印，防止哈希漂移

## 策略

1. 使用 jq --sort-keys 递归排序 JSON 所有层级
2. 移除所有空白字符，生成规范格式
3. 计算 SHA256 哈希作为数字钢印
4. 存储 canonical.json + steel-seal.sha256 双文件
5. 验证时重新计算哈希并比对
6. 确保不同环境生成相同哈希值

## 约束

```json
{
  "algorithm": "SHA256",
  "format": "canonical JSON",
  "tool": "jq + sha256sum"
}
```

## 验证命令

```bash
./canonical-seal --verify input.json
```

## 使用场景

- 资产发布前固化
- 跨环境哈希验证
- 防止哈希漂移

## 负熵指标

| 指标 | 目标 | 说明 |
|------|------|------|
| 哈希一致性 | 100% | 跨环境相同 |
| 验证通过率 | 100% | 钢印有效 |
| 漂移检测 | 0 | 无漂移 |
| 负熵评分 | 9.7/10 | 帝国链量化指标 |


## 相關文檔

- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[03-evomap_drift_pre_scan]]
- [[03-openclaw_config_schema_verify]]
