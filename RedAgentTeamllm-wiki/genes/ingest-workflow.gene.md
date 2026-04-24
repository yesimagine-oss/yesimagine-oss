# Gene: Ingest Workflow

**gene_id**: `GENE_003_INGEST_WORKFLOW`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04  
**category**: 工作流  
**risk_level**: low  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T05:45:00Z

---

## 📝 Summary

Ingest: read raw → summarize → update entities/concepts → refresh index.md → append log.md.

編譯工作流：讀取原始資料 → 摘要 → 更新實體/概念 → 刷新索引 → 追加日志。

---

## 🎯 Content

**Ingest 工作流定義**:

當人類向 `raw/` 添加新文檔時，LLM 必須執行以下編譯流程:

### 階段 1: 讀取 (Read)
- 檢測 raw/ 中的新文件
- 完整讀取文件內容
- 記錄文件元數據 (名稱、大小、創建時間)

### 階段 2: 摘要 (Summarize)
- 提取核心觀點
- 識別關鍵實體 (人名、地名、概念、技術)
- 生成 200-500 字摘要

### 階段 3: 更新實體/概念 (Update Entities/Concepts)
- 檢查 wiki/ 中是否已存在相關條目
- 如存在：更新現有條目，添加新信息
- 如不存在：創建新條目
- 建立交叉引用 (cross-references)

### 階段 4: 刷新索引 (Refresh index.md)
- 更新 wiki/index.md
- 將新條目歸類到正確分類
- 更新相關標籤

### 階段 5: 追加日志 (Append log.md)
- 在 log.md 中記錄本次編譯
- 包含：時間、源文件、創建/更新的條目數
- Git commit 所有變更

**編譯質量標準**:

- 每個 raw 文檔必須生成至少 1 個 wiki 條目
- 每個條目必須有來源引用
- 必須建立交叉引用 (至少 1 個相關條目)
- 必須更新索引
- 必須追加日志

**24 小時規則**:

新 raw 文檔必須在 24 小時內完成編譯，否則觸發警告。

---

## 🧬 Signals

`ingest`, `workflow`, `knowledge_compilation`, `summarize`, `entities`, `concepts`, `index_update`, `log_append`, `AOT`, `24h_rule`

---

## 📋 Strategy

### 步驟 1: 監控 Raw 目錄
定期掃描 raw/ 目錄，檢測新添加的文件。

### 步驟 2: 讀取並分析
讀取新文件，提取核心內容和關鍵實體。

### 步驟 3: 創建/更新 Wiki 條目
根據分析結果，創建或更新 wiki 條目。

### 步驟 4: 建立交叉引用
在新舊條目之間建立雙向引用。

### 步驟 5: 更新索引和日志
刷新 index.md，追加 log.md，Git commit。

---

## ✅ Validation

```bash
# 1. 檢查是否有未編譯的 raw 文檔
find /home/admin/.openclaw/workspace/llm-wiki/raw -name "*.md" -mtime -1 -type f

# 2. 檢查 log.md 是否有編譯記錄
grep -i "ingest\|編譯" /home/admin/.openclaw/workspace/llm-wiki/log.md | tail -5

# 3. 檢查 index.md 是否更新
grep -l "2026-04-17" /home/admin/.openclaw/workspace/llm-wiki/wiki/index.md

# 4. 檢查 wiki 條目是否有來源引用
grep -l "來源\|source" /home/admin/.openclaw/workspace/llm-wiki/wiki/*.md | head -5

# 5. 檢查 Git 提交記錄
cd /home/admin/.openclaw/workspace && git log --oneline -5 -- llm-wiki/raw/ llm-wiki/wiki/
```

---

## 🔒 Constraints

- **必須**: 新 raw 文檔 24 小時內完成編譯
- **必須**: 每個編譯必須創建至少 1 個 wiki 條目
- **必須**: 每個 wiki 條目必須有來源引用
- **必須**: 必須建立交叉引用
- **必須**: 必須更新 index.md
- **必須**: 必須追加 log.md
- **禁止**: 跳過任何步驟
- **禁止**: 修改 raw/ 原始文件

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| 24h 編譯率 | 100% | 待測量 |
| 平均每文檔條目數 | ≥1 | 待測量 |
| 交叉引用率 | >80% | 待測量 |
| 索引更新率 | 100% | 待測量 |
| 日志追加率 | 100% | 待測量 |

---

## 🔗 References

- RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04
- `GENE_001_REDAGENTTEAMLLM-WIKI_CORE_IDEAL`
- `GENE_002_THREE_LAYER_ARCHITECTURE`
- `/home/admin/.openclaw/workspace/llm-wiki/schema.md`

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8
