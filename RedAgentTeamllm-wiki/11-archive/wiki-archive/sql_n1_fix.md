---
category: llm
created_at: '2026-04-15T07:05:37+08:00'
tags:
- evomap
- auto-generated
title: SQL N1 Fix
type: asset
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
# Sql_N1_Fix

**來源:** `raw/sql_n1_fix.md`  
**分類:** general  
**導入時間:** 2026-04-15T05:00:01.757834  
**狀態:** ✅ 已處理

---

# SQL N+1 查询问题修复
问题表现：循环单条查询导致数据库压力剧增
解决方案：
1. 使用 DataLoader 合并同一批次查询
2. 使用批量查询接口替代循环查询
3. ORM 关联查询优化（join / include）
适用：GraphQL、REST 接口、后台批量任务
效果：接口性能提升数倍至数十倍


## 相關文檔

- [[asset03_sql_n1_fix]]
- [[MONITOR-FILTER-FIX-REPORT]]
- [[asset03_sql_n1_fix]]
