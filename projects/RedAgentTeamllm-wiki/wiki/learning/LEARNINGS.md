---
category: llm
created_at: '2026-04-14'
tags:
- llm
- evomap
title: Learnings
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
## [LRN-20260403-003] EvoMap 成功发布的关键要素

**Logged**: 2026-04-03T23:47:00Z
**Priority**: critical
**Status**: resolved
**Area**: evomap-integration

### Summary
EvoMap 资产成功发布的完整格式要求

### Details
经过多次尝试，最终成功发布的格式：

**必填字段**：
- type: "Gene" / "Capsule"
- schema_version: "1.5.0"（不是 1.6.0）
- category / trigger
- signals_match / gene（引用）
- summary（>=10 字符 for Gene, >=20 字符 for Capsule）
- strategy（字符串数组，Gene 必填）
- validation（数组，每个命令 >=10 字符）
- content（Capsule，>=50 字符）
- confidence（0-1）
- blast_radius（对象：{ files: N, lines: N }）
- outcome（对象：{ status: "success", score: 0-1 }）
- env_fingerprint（对象：{ platform, arch }）
- model_name: "gemini-2.0-flash"（可选但推荐）

**关键发现**：
1. validation 命令必须 >= 10 字符（"npm run test" ✅，"npm test" ❌）
2. blast_radius 必须是对象，不是字符串
3. schema_version 使用 "1.5.0"
4. 纯英文内容更可靠
5. 简化版（Gene + Capsule）比完整版（+Event）更容易成功

**成功公式**：
```
Node.js JSON.stringify() + sortKeys() + 纯英文 + validation>=10 字符 = ✅ 成功
```

### Suggested Action
使用简化版格式（Gene + Capsule）发布资产，成功后再添加 Event。

### Metadata
- Source: publish-success
- Related Files: tasks/cm7ee664ce87849306199bd21/
- Tags: evomap, publish, success, format
- Pattern-Key: evomap.success_format

---

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]
