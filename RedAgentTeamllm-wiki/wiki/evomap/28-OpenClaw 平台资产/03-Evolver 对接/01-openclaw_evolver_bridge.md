---
category: innovate
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- evolver
- bridge
- gep
title: OpenClaw Evolver 桥接
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
# Capsule: openclaw_evolver_bridge

## 触发条件

资产固化上链

## 执行流程

```bash
# 1. 验证资产
openclaw-cli asset verify

# 2. 导入到 GEP 链
gep_import --from openclaw --chain-id openclaw_ai_full_20260415

# 3. 确认上链
verify_chain_status()
```

## 输出

- 上链结果
- 资产哈希
- Chain ID

## 使用场景

- 资产固化
- EvoMap 集成
- 知识上链


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[Evolver 架构]]
