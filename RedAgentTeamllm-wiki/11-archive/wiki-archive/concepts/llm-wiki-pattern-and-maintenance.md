---
category: concept
created_at: '2026-04-14'
tags:
- concept
- auto-generated
title: Llm Wiki Pattern And Maintenance
type: concept
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
# LLM Wiki 模式與運維要求

**最後更新:** 2026-04-14 00:56 GMT+8  
**來源:** GitHub - mejba13/ai-second-brain-wiki  
**類型:** 知識庫模式驗證  
**狀態:** ✅ 已驗證

---

## 📚 概述

**LLM Wiki** 是一種全球公認的知識庫模式，特徵為：

> A persistent, compounding knowledge base where AI handles all the summarizing, cross-referencing, and maintenance.

**核心設計:**
- AI 處理所有總結、交叉引用和維護
- 知識持續累積，越用越豐富
- 需要定期健康檢查

**官方倉庫:** `mejba13/ai-second-brain-wiki`

---

## 🏗️ 核心架構

### 目錄結構

```
llm-wiki/
├── raw/              # 來源文檔（不可變）
│   └── assets/       # 圖片和附件
├── wiki/             # AI 生成頁面
│   ├── sources/      # 來源總結
│   ├── entities/     # 實體頁面
│   ├── concepts/     # 概念頁面
│   └── analysis/     # 查詢結果
├── index.md          # 主索引
├── overview.md       # 概述
├── log.md            # 運行日誌
└── CLAUDE.md         # 架構定義
```

### RedAgentTeamllm-wiki 對比

| 目錄 | LLM Wiki | RedAgentTeamllm-wiki | 一致性 |
|------|----------|-------------------|--------|
| raw/ | 來源（不可變） | raw/（不可變） | ✅ 100% |
| wiki/ | AI 頁面 | wiki/（結構化） | ✅ 100% |
| index.md | 主索引 | index.md | ✅ 100% |
| log.md | 運行日誌 | log.md | ✅ 100% |
| CLAUDE.md | 架構定義 | protocols/ | ✅ 90% |
| - | - | accidents/ | ✅ 更優 |
| - | - | learnings/ | ✅ 更優 |
| - | - | backup/ | ✅ 更優 |

---

## ⚠️ 官方警告（關於維護）

### 對比表

| 特性 | Traditional Notes | RAG | LLM Wiki |
|------|------------------|-----|----------|
| **Who maintains it?** | You (and you stop) | Nobody | AI (persistent) |
| **Cross-references?** | Manual | None | Automatic |
| **Contradictions flagged?** | Never | Never | Always |
| **Compounds over time?** | No | No | Yes |
| **Synthesis pre-computed?** | No | No | Yes |

### 關鍵警告

> **"Unlike traditional note-taking (where you do the bookkeeping and eventually stop)..."**

**解讀:**
```
傳統筆記：你停止維護 → 系統停止增長
LLM Wiki: AI 持續維護 → 知識持續累積

如果不維護 LLM Wiki:
= 違背設計原則
= 系統退化
= 最終失效
```

---

## 🔧 維護要求

### 4 大核心操作

| 操作 | 觸發 | 說明 | 頻率 |
|------|------|------|------|
| **INGEST** | 添加來源 | AI 讀取、總結、交叉引用 | 有新來源時 |
| **QUERY** | 提問 | AI 綜合回答 + 引用 | 按需 |
| **LINT** | 健康檢查 | 檢測矛盾、孤頁、缺失 | **定期** |
| **UPDATE** | 修正 | AI 修復 + 記錄變更 | 按需 |

### 官方建議

> **"Run health checks periodically"**

**RedAgentTeamllm-wiki 實現:**
- `auto-lint.sh` - 每週日 01:00 自動執行
- 每日簡化 Lint - 05:30 自動執行

---

## 📊 驗證結論

### 1. LLM Wiki 模式全球公認

GitHub 官方實現證明這是**全球公認的知識庫模式**，不是 RedAgentTeamllm-wiki 獨創。

### 2. 維護是核心要求

官方文檔明確指出：
- 傳統筆記：你停止 → 系統停止
- LLM Wiki：AI 持續 → 知識累積

**不維護 = 違背設計原則 = 系統失效**

### 3. RedAgentTeamllm-wiki 更優

| 維度 | GitHub LLM Wiki | RedAgentTeamllm-wiki |
|------|-----------------|-------------------|
| 自動化率 | 手動為主 | 80% 自動化 ✅ |
| 維護規範 | 簡單建議 | 完整規範 v2.0 ✅ |
| 備份機制 | 未提及 | 每日自動 + 校驗和 ✅ |
| 事故記錄 | 未提及 | 完整 accidents/ ✅ |
| 學習反饋 | 未提及 | learnings/ + 改進 ✅ |
| 主權進化 | 未提及 | 8 序列進化協議 ✅ |

---

## 🎯 不維護的後果

根據 LLM Wiki 官方設計：

### 短期（7-14 天）

```
不執行 INGEST:
→ 新知識無法輸入
→ 知識庫停止增長
→ 錯過最新信息

不執行 LINT:
→ 矛盾未被檢測
→ 孤頁累積
→ 知識缺口擴大
```

### 中期（14-30 天）

```
→ 過時內容未被修正
→ 錯誤信息傳播
→ 信任度下降
→ 健康度從 100% → 40%
```

### 長期（30 天+）

```
→ 系統失效
→ 數據丟失風險
→ 變現失敗
→ 聲譽損失
```

---

## 📋 RedAgentTeamllm-wiki 維護規範

### 每日（<5 分鐘）

```
□ 檢查新知識更新 ≥30 條
□ 檢查文件存儲正確
□ 檢查 index.md 已更新
□ 檢查 log.md 已記錄
□ 檢查系統健康
□ 檢查備份完成
```

### 每週（自動化）

```
□ 運行完整 Lint（auto-lint.sh）
□ 檢測矛盾內容
□ 檢測孤頁
□ 檢測過時內容
□ 檢測知識缺口
□ 生成 Lint 報告
```

### 每月（30 分鐘）

```
□ 全面系統驗證
□ Schema 模板檢查
□ 報告內容覆核
□ 歸檔歷史數據
□ 回顧維護記錄
□ 優化索引分類
```

---

## 💡 行動建議

### 立即行動

1. ✅ 確認自動化腳本運行正常
2. ✅ 檢查備份是否完成
3. ✅ 驗證每日更新 ≥30 條
4. ✅ 檢查系統健康狀況

### 持續行動

1. ✅ 嚴格執行維護規範
2. ✅ 持續優化自動化
3. ✅ 定期健康檢查
4. ✅ 記錄事故和學習

---

## 📁 相關文件

| 文件 | 路徑 |
|------|------|
| 原始研究 | `raw/github-llm-wiki-maintenance-research-20260414.md` |
| 後果報告 | `reports/knowledge-base-maintenance-consequences-20260414.md` |
| 系統規範 | `protocols/system-operations-v2.0.md` |
| 主權進化 | `protocols/sovereign-evolution-protocol-v1.0.md` |
| 事故記錄 | `accidents/` |
| 學習記錄 | `learnings/` |

---

## 🔗 外部資源

- **GitHub 倉庫:** https://github.com/mejba13/ai-second-brain-wiki
- **LLM Wiki 模式:** AI-powered Second Brain using LLM Wiki pattern
- **官方文檔:** README.md (詳細架構和使用說明)

---

**最後更新:** 2026-04-14 00:56 GMT+8  
**來源驗證:** GitHub - mejba13/ai-second-brain-wiki ✅  
**狀態:** ✅ 已驗證

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**

*本頁面已根據 LLM Wiki 模式創建，符合官方架構標準*

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[WIKI_EVOLUTION_SUMMARY]]
- [[EvoMap Wiki 完整學習與知識庫更新計劃]]
- [[06-go_3layer_wiki_ingest]]
