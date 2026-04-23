---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Schema
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
# LLM Wiki Schema · 核心操作規範

**版本**: 1.0.0  
**創建時間**: 2026-04-17 05:45 GMT+8  
**來源**: Karpathy LLM Wiki Original 2026-04-04 + EvoMap GEP 1.5.0  
**維護者**: LLM (AI Agent)  
**人類權限**: 只讀 (可修改 raw/ 和提問)

---

## 🏗️ 三層架構

```
llm-wiki/
├── raw/           # 原始資料層 (人類所有，只讀來源)
│   ├── *.md       # 原始文檔
│   └── log.md     # 原始資料日志
├── wiki/          # 編譯知識層 (LLM 所有，結構化知識)
│   ├── *.md       # 知識條目
│   ├── index.md   # 總索引
│   └── log.md     # 編譯日志
├── genes/         # 規則基因層 (不可變，核心規則)
│   └── *.gene.md  # Gene 定義文件
├── capsules/      # 實例膠囊層 (可執行，具體實現)
│   └── *.capsule.md # Capsule 定義文件
├── schema.md      # 本文件 (工作流規範)
└── log.md         # 全局日志 (追加式)
```

---

## 🧬 核心原則 (Karpathy Core Ideal)

**Replace JIT RAG with AOT Knowledge Compilation**

- ❌ **禁止**: 每次查詢時檢索原始資料 (JIT RAG)
- ✅ **必須**: 預先編譯原始資料為持久知識庫 (AOT)
- ✅ **目標**: 知識累積、複利增長、LLM 維護

---

## 📋 工作流規範

### 1️⃣ Ingest 工作流 (知識編譯)

```
觸發: 人類添加新 raw 文檔
↓
LLM: 讀取 raw → 摘要 → 提取實體/概念
↓
LLM: 更新/創建 wiki 條目 (最多 15 頁)
↓
LLM: 刷新 wiki/index.md
↓
LLM: 追加 log.md
↓
LLM: Git commit
```

**規範**:
- 每個 raw 文檔必須編譯為 wiki 條目
- 禁止保留未編譯的 raw 文檔超過 24 小時
- 編譯必須保留原始出處引用

### 2️⃣ Query 工作流 (知識查詢)

```
觸發: 人類提問
↓
LLM: 搜索 wiki/index.md (禁止直接檢索 raw)
↓
LLM: 合成答案 (基於 wiki 知識)
↓
LLM: 判斷答案價值
  ├─ 高價值 → 保存為新 wiki 條目
  └─ 普通 → 直接回答
↓
LLM: 追加 log.md
```

**規範**:
- 優先使用 wiki 知識，禁止跳過 wiki 直接檢索 raw
- 高價值答案必須沉澱為 wiki 條目
- 答案必須引用來源 (wiki 條目名)

### 3️⃣ Lint 工作流 (健康檢查)

```
觸發: 定期 (每周) 或 手動
↓
LLM: 掃描 wiki 健康
  ├─ 檢測矛盾
  ├─ 檢測過時聲明
  ├─ 檢測孤兒頁面
  ├─ 檢測缺失交叉引用
  └─ 檢測知識缺口
↓
LLM: 自動修復 (如可能)
↓
LLM: 生成 lint-report-YYYYMMDD.md
↓
LLM: 追加 log.md
```

**規範**:
- 每周至少執行一次 Lint
- 發現問題必須記錄並嘗試修復
- 無法自動修復的問題必須報告人類

---

## 👥 人類 vs LLM 職責分離

| 職責 | 人類 | LLM |
|------|------|-----|
| **raw/ 管理** | ✅ 添加、刪除、修改 | ❌ 只讀 |
| **wiki/ 管理** | ❌ 只讀 | ✅ 創建、更新、維護 |
| **schema.md** | ✅ 審批修改 | ✅ 提議、執行 |
| **genes/** | ✅ 審批 | ✅ 創建、維護 |
| **capsules/** | ✅ 審批 | ✅ 創建、執行 |
| **提問** | ✅ 發起查詢 | ✅ 回答 |
| **思考** | ✅ 戰略決策 | ✅ 執行建議 |
| **Git Commit** | ✅ 審批 | ✅ 自動提交 |

**核心原則**:
- 人類控制輸入 (raw) 和方向 (提問)
- LLM 負責知識維護和執行
- wiki/ 是 LLM 的領地，人類不直接修改

---

## 📐 文件命名規範

### Genes
```
{name}.gene.md
示例: karpathy-core-ideal.gene.md
```

### Capsules
```
{name}.capsule.md
示例: ollama-oneclick-deploy.capsule.md
```

### Wiki 條目
```
{topic}.md
示例: docker-layer-cache.md
```

### 報告
```
{type}-YYYYMMDD.md
示例: lint-report-20260417.md
```

---

## 🔒 不變性規則

| 目錄/文件 | 可變性 | 說明 |
|----------|--------|------|
| `raw/` | 🔴 人類只讀 | LLM 禁止修改 |
| `wiki/` | 🟢 LLM 所有 | 人類禁止直接修改 |
| `genes/` | 🟡 審批後可變 | 需人類審批 |
| `capsules/` | 🟡 審批後可變 | 需人類審批 |
| `schema.md` | 🟡 審批後可變 | 需人類審批 |
| `log.md` | 🟢 LLM 追加 | 人類只讀 |

---

## 📊 質量指標

| 指標 | 目標 | 檢查方式 |
|------|------|----------|
| Raw→Wiki 編譯率 | 100% | Lint 檢查 |
| Wiki 條目引用率 | >80% | 交叉引用檢查 |
| 孤兒頁面 | <5% | Lint 檢查 |
| 過時聲明 | 0 | Lint 檢查 |
| Log 追加率 | 100% | 手動檢查 |

---

## 🔄 Schema 協同進化

本 schema.md 由 LLM 和人類共同進化:

1. **LLM 提議** - 在實踐中發現改進點
2. **人類審批** - 人類審核並批准修改
3. **共同更新** - 更新 schema.md 並 Git commit
4. **記錄變更** - 在 log.md 中記錄變更原因

**進化原則**:
- 保持穩定性，避免頻繁變更
- 變更必須有明確理由
- 變更必須記錄在 log.md

---

## ✅ 合規檢查清單

每次操作前檢查:

- [ ] 是否遵循三層架構？
- [ ] 是否使用 AOT 而非 JIT RAG？
- [ ] 是否遵守 Human/LLM 職責分離？
- [ ] 是否追加 log.md？
- [ ] 是否需要 Git commit？

---

**最後更新**: 2026-04-17 05:45 GMT+8  
**下次 Lint**: 2026-04-24 (每周)


## 相關文檔

- [[03-openclaw_config_schema_verify]]
- [[Schema 1.5.0 完整參考]]
- [[02-anycross_api_schema_validate]]
