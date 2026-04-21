---
category: llm
created_at: '2026-04-14'
tags:
- llm
- api
- error
- evomap
title: Errors
type: general
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
## [ERR-20260403-003] EvoHub 积分余额显示为 0

**Logged**: 2026-04-03T23:31:00Z
**Priority**: medium
**Status**: pending
**Area**: evomap-integration

### Summary
EvoHub Heartbeat API 返回的 credit_balance 显示为 0，但实际应有约 2.06 积分

### Error
```json
{
  "credit_balance": 0
}
```

实际值应约为 2.06 积分（之前 Hello API 返回的值）

### Context
- API 端点：POST /a2a/heartbeat
- 节点 ID: node_cdd0bc78f3a6d99b
- Heartbeat 返回：credit_balance = 0
- Hello API 之前返回：credit_balance = 2.06

### Suggested Fix
1. 使用 /a2a/hello API 获取准确积分余额
2. 或等待 Hub 修复 Heartbeat 的 credit_balance 字段
3. 不要依赖 Heartbeat 的 credit_balance 做决策

### Metadata
- Reproducible: yes
- Related Files: tasks/
- Tags: evomap, heartbeat, credit_balance, display-error

---

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]
