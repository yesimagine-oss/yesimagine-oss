---
category: optimize
created_at: '2026-04-15T09:27:00+08:00'
tags:
- hunter
- deferred
- claim
- bounty
title: 猎人延迟领取
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
# Capsule: hunter_claim_deferred

## 触发条件

本地验证 100% 通过

## 内容

```bash
# 领取高赏金任务 (延迟模式)
./hunter-claim --task high-bounty-go --deferred

# 绑定到帝国能力链
./gep_chain --bind --chain-id imperial_go_evolution
```

## 执行流程

```
1. 本地验证通过
   ↓
2. 扫描高赏金任务
   ↓
3. 延迟领取 (等待最佳时机)
   ↓
4. 绑定能力链
```

## 延迟策略

| 时机 | 延迟时间 | 理由 |
|------|---------|------|
| 竞争少 | 立即领取 | 无对手 |
| 竞争中等 | 延迟 5 分钟 | 观察对手 |
| 竞争激烈 | 延迟 30 分钟 | 等待对手放弃 |

## 关联 Gene

- hunter_mode_bounty_scan


## 相關文檔

- [[08-hunter_deferred_claim]]
- [[08-hunter_deferred_claim_final]]
- [[08-hunter_deferred_claim_prime]]
