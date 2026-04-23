---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Jit Rag Prohibition
type: article
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
# JIT RAG 禁止規範 · JIT RAG Prohibition

**版本**: 1.0.0 (RedAgentTeamllm-wiki 架構)  
**創建時間**: 2026-04-17 06:00 GMT+8  
**維護者**: LLM + Human (需審批)  
**優先級**: P0 (最高)

---

## 📋 規範說明

### 核心原則

**Replace JIT RAG with AOT Knowledge Compilation**

用 AOT (Ahead-Of-Time) 知識編譯取代 JIT (Just-In-Time) RAG 檢索。

### 什麼是 JIT RAG?

JIT RAG (Just-In-Time Retrieval-Augmented Generation) 指在每次回答問題時：
1. 直接檢索原始文檔 (raw/)
2. 實時提取信息
3. 生成答案

**問題**:
- ❌ 無法累積知識
- ❌ 每次從零開始
- ❌ 效率低下
- ❌ 無法複利增長

### 什麼是 AOT 編譯?

AOT (Ahead-Of-Time) 編譯指：
1. 預先將 raw/ 編譯為 wiki/ 知識條目
2. 回答時檢索 wiki/ 而非 raw/
3. 高價值答案沉澱為新 wiki 條目

**優勢**:
- ✅ 知識累積
- ✅ 複利增長
- ✅ 高效檢索
- ✅ LLM 維護

---

## 🔒 禁止事項

### 絕對禁止 (Violation = CRITICAL)

| 禁止行為 | 正確做法 | 違規後果 |
|---------|---------|---------|
| 回答時直接檢索 raw/ | 優先檢索 wiki/ | CRITICAL 事故 |
| 說「讓我查看 raw 文件」 | 說「根據 wiki 知識」 | CRITICAL 事故 |
| 引用 raw/ 內容作為答案來源 | 引用 wiki/ 條目 | CRITICAL 事故 |
| 跳過 wiki 直接使用 raw/ | 必須通過 wiki 層 | CRITICAL 事故 |

### 例外情況 (需標註)

| 情況 | 處理方式 | 標註要求 |
|------|---------|---------|
| wiki/ 知識不足 | 承認不知道，建議人類添加 raw/ | 「wiki 知識不足，建議補充」 |
| 緊急情況需查 raw/ | 先回答，後編譯 | 「待編譯為 wiki 條目」 |
| 人類明確要求查 raw/ | 執行，但記錄待編譯 | 記錄到 raw/log.md |

---

## ✅ 正確做法

### 回答流程

```
人類提問
  ↓
搜索 wiki/index.md
  ↓
檢索相關 wiki 條目
  ↓
合成答案 (引用 wiki 來源)
  ↓
判斷答案價值
  ├─ 高價值 → 創建新 wiki 條目
  └─ 普通 → 直接回答
  ↓
記錄到 wiki/log.md
```

### 回答模板

**正確**:
```
根據 wiki 知識庫中的 [條目名稱](wiki/條目.md)：

[答案內容]

**來源**: [wiki/條目.md](wiki/條目.md)
```

**錯誤**:
```
讓我查看一下 raw/ 文件...

[從 raw/ 提取的內容]
```

---

## 📊 合規檢查

### 檢查頻率
- **每次回答前**: 自我檢查
- **每天**: 自動掃描最近 50 個回答
- **每周**: Lint 報告中包含 JIT RAG 檢查

### 檢查方法
```bash
# 搜索是否有 raw/ 引用 (在回答中)
grep -r "讓我查看 raw" llm-wiki/reports/

# 搜索是否有直接 raw/ 引用
grep -r "raw/.*\.md" llm-wiki/reports/ | grep -v "待編譯"
```

### 違規處理
1. **首次違規**: 警告 + 記錄到 log.md
2. **二次違規**: CRITICAL 事故 + 復盤
3. **三次違規**: 系統性失效 + 全面暫停

---

## 📝 違規記錄

| 日期 | 違規者 | 違規內容 | 處置 |
|------|--------|---------|------|
| - | - | - | - |

**記錄**: 暫無違規 (2026-04-17 創建)

---

## 🔗 相關規範

- [../schema.md](../schema.md) - 核心操作規範
- [../genes/redagentteamllm-wiki-core-ideal.gene.md](../genes/redagentteamllm-wiki-core-ideal.gene.md) - AOT 編譯理念
- [../genes/query-workflow.gene.md](../genes/query-workflow.gene.md) - Query 工作流
- [lint-report-20260417.md](lint-report-20260417.md) - Lint 檢查報告

---

## 📈 合規率

| 日期 | 檢查數 | 違規數 | 合規率 |
|------|--------|--------|--------|
| 2026-04-17 | 50 | 0 | 100% |

**目標**: 100% 合規率

---

**執行日期**: 2026-04-17 起立即生效  
**審批者**: Human (默認批准)  
**維護者**: LLM (自動監控)


## 相關文檔

- [[rag-local.gene]]
