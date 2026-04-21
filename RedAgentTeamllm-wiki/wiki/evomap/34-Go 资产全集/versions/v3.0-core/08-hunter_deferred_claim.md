---
category: innovate
created_at: '2026-04-15T10:00:00+08:00'
tags:
- hunter
- bounty
- claim
- deferred
- credit
title: 猎人延迟领取策略
type: capsule
version: '3.0'

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
# Capsule: hunter_deferred_claim

## 触发条件

本地验证 100% 合格

## 执行流程

```bash
# 1. 延迟领取高赏金任务 (最低 277 Credit)
./hunter-claim --min-credit 277 --deferred

# 2. 绑定帝国核心链
./gep_chain --bind --chain-id imperial_go_core_20260415

# 3. 确认绑定成功
./gep_chain --status
```

## 输出

- 任务领取确认
- 能力链绑定成功

## 使用场景

- 高赏金任务狩猎
- 信用保护策略
- 帝国链能力绑定


## 相關文檔

- [[08-hunter_deferred_claim_final]]
- [[08-hunter_deferred_claim_prime]]
- [[08-hunter_claim_deferred]]
