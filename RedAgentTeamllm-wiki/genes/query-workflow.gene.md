# Gene: Query Workflow

**gene_id**: `GENE_004_QUERY_WORKFLOW`  
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

Query: search wiki index → synthesize answer → file valuable answers back into wiki as new pages.

查詢工作流：搜索知識庫索引 → 合成答案 → 將高價值答案存儲為新知識頁面。

---

## 🎯 Content

**Query 工作流定義**:

當人類提出問題時，LLM 必須執行以下查詢流程:

### 階段 1: 搜索索引 (Search Wiki Index)
- 搜索 wiki/index.md 找到相關條目
- 檢索相關 wiki 條目內容
- **禁止**: 直接檢索 raw/ 文檔 (JIT RAG)

### 階段 2: 合成答案 (Synthesize Answer)
- 基於 wiki 知識合成答案
- 引用來源條目 (必須)
- 如知識不足，承認不知道

### 階段 3: 價值評估 (Evaluate Value)
判斷答案是否值得存儲為新知識:

**高價值標準**:
- 通用性強 (不僅適用於當前問題)
- 結構化程度高 (可獨立成文)
- 填補知識空白
- 未來可能被再次詢問

### 階段 4: 沉澱知識 (File Back into Wiki)
如答案為高價值:
- 創建新 wiki 條目
- 添加到 index.md 正確分類
- 建立交叉引用
- 追加 log.md
- Git commit

**為什麼重要**:

- 確保答案基於已驗證知識 (wiki)
- 避免重複回答相同問題
- 知識庫隨使用而增長
- 形成知識複利效應

**與 Ingest 的區別**:

- Ingest: raw→wiki (人類輸入驅動)
- Query: 問題→答案→wiki (問題驅動)
- 兩者互補，共同豐富知識庫

---

## 🧬 Signals

`query`, `workflow`, `wiki_search`, `answer_synthesis`, `knowledge沉淀`, `high_value`, `compounding`, `AOT`, `no_JIT_RAG`, `cross_reference`

---

## 📋 Strategy

### 步驟 1: 接收問題
理解人類提出的問題，提取關鍵詞和意圖。

### 步驟 2: 搜索 Wiki
在 wiki/index.md 中搜索相關條目，檢索內容。

### 步驟 3: 合成答案
基於 wiki 知識合成完整答案，引用來源。

### 步驟 4: 評估價值
判斷答案是否符合高價值標準。

### 步驟 5: 沉澱知識
如為高價值，創建新 wiki 條目並更新索引。

---

## ✅ Validation

```bash
# 1. 檢查是否有 Q&A 形式的 wiki 條目
grep -l "問題\|Q&A\|問答" /home/admin/.openclaw/workspace/llm-wiki/wiki/*.md | head -5

# 2. 檢查答案是否有來源引用
grep -c "來源\|參見\|reference" /home/admin/.openclaw/workspace/llm-wiki/wiki/*.md | sort -rn | head -10

# 3. 檢查 log.md 是否有查詢記錄
grep -i "query\|查詢\|問題" /home/admin/.openclaw/workspace/llm-wiki/log.md | tail -5

# 4. 檢查 index.md 是否有 Q&A 分類
grep -i "Q&A\|問答\|常見問題" /home/admin/.openclaw/workspace/llm-wiki/wiki/index.md

# 5. 檢查 Git 提交中是否有新 wiki 條目
cd /home/admin/.openclaw/workspace && git log --oneline --diff-filter=A -- llm-wiki/wiki/ | head -10
```

---

## 🔒 Constraints

- **禁止**: 直接檢索 raw/ 回答問題 (JIT RAG)
- **必須**: 答案必須引用 wiki 來源
- **必須**: 高價值答案必須沉澱為 wiki 條目
- **必須**: 新條目必須更新 index.md
- **必須**: 必須追加 log.md
- **禁止**: 承認知道但實際不知道 (反幻覺)
- **必須**: 知識不足時承認不知道

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| Wiki 搜索率 | 100% | 待測量 |
| 答案引用率 | 100% | 待測量 |
| 高價值沉澱率 | >50% | 待測量 |
| 知識不足承認率 | 100% | 待測量 |
| 重複問題減少率 | >30%/月 | 待測量 |

---

## 🔗 References

- RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04
- `GENE_001_REDAGENTTEAMLLM-WIKI_CORE_IDEAL`
- `GENE_003_INGEST_WORKFLOW`
- `/home/admin/.openclaw/workspace/llm-wiki/schema.md`

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8
