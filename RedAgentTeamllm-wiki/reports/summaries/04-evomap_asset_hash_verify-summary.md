---
title: "EvoMap 资产哈希验证"
type: "gene"
category: "optimize"
tags: ["evomap", "hash_verify", "sha256", "integrity"]
created_at: "2026-04-15T08:40:00+08:00"
version: "1.0"
---

# Gene: evomap_asset_hash_verify

## 摘要

验证资产 sha256 唯一性与元数据完整性

## 策略

1. 使用 canonical JSON 计算 asset_id
2. 验证 sha256 格式正确 (sha256:64hex)
3. 检查 asset_id 与内容匹配
