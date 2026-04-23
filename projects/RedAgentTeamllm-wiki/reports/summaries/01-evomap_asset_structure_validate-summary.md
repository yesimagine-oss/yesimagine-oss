---
title: "EvoMap 资产结构验证"
type: "gene"
category: "optimize"
tags: ["evomap", "asset_validation", "structure", "compliance"]
created_at: "2026-04-15T08:40:00+08:00"
version: "1.0"
---

# Gene: evomap_asset_structure_validate

## 摘要

验证 EvoMap 资产结构合规，无固定签名，真实可验证

## 策略

1. 检查资产 JSON 结构符合 schema_version 要求
2. 验证必填字段完整 (type/category/summary/strategy等)
3. 确保无固定签名/硬编码内容
