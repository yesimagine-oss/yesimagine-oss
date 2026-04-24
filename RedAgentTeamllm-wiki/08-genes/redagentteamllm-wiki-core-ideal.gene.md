# Gene: RedAgentTeamllm-wiki Core Ideal

**gene_id**: `GENE_001_REDAGENTTEAMLLM-WIKI_CORE_IDEAL`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04  
**category**: 知識庫架構  
**risk_level**: low  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T05:45:00Z

---

## 📝 Summary

Replace JIT RAG (retrieve-every-query) with AOT knowledge compilation: build a persistent, compounding wiki maintained by LLM, not human.

用 AOT (Ahead-Of-Time) 知識編譯取代 JIT RAG (Just-In-Time Retrieval): 構建由 LLM 維護的持久、複利增長的知識庫。

---

## 🎯 Content

**核心理念**:

傳統的 RAG (Retrieval-Augmented Generation) 在每次查詢時都從原始文檔中檢索信息，這種方式效率低下且無法累積知識。

RedAgentTeamllm-wiki 提出的 AOT (Ahead-Of-Time) 編譯模式要求:

1. **預先編譯** - 在查詢前將所有原始資料編譯為結構化知識
2. **持久存儲** - 知識以 Markdown 形式持久化，可版本控制
3. **LLM 維護** - 由 LLM 負責知識的更新、維護和質量控制
4. **複利增長** - 每次編譯都增強知識庫，形成知識複利

**為什麼重要**:

- JIT RAG 每次查詢都從零開始，無法累積
- AOT 編譯讓知識庫隨時間增長而變得更強大
- LLM 維護確保知識的及時性和準確性
- Markdown + Git 讓知識可審計、可回溯

**與 EvoMap 的關係**:

- Gene 是不可變的規則定義
- 此 Gene 是知識庫架構的基礎規則
- 所有 Capsule 必須遵守此 Gene 的原則

---

## 🧬 Signals

`RedAgentTeamllm-wiki`, `AOT`, `JIT_RAG`, `knowledge_compilation`, `persistent_wiki`, `LLM_maintained`, `compounding_knowledge`, `markdown_git`, `EvoMap_Gene`, `architecture`

---

## 📋 Strategy

### 步驟 1: 識別 JIT RAG 問題
檢測當前系統是否在每次查詢時檢索原始文檔。如是，標記為需要 AOT 編譯。

### 步驟 2: 建立三層架構
創建 raw/ (原始資料), wiki/ (編譯知識), schema.md (規範) 三層結構。

### 步驟 3: 編譯原始資料
讀取 raw/ 中的所有文檔，摘要、提取實體、創建 wiki 條目。

### 步驟 4: 建立索引
創建 wiki/index.md，包含所有知識條目的分類索引。

### 步驟 5: 啟用 LLM 維護
配置 LLM 自動更新 wiki、執行 Lint、追加 log.md。

---

## ✅ Validation

```bash
# 1. 檢查三層架構是否存在
ls -la /home/admin/.openclaw/workspace/llm-wiki/{raw,wiki}/

# 2. 檢查 schema.md 是否存在
test -f /home/admin/.openclaw/workspace/llm-wiki/schema.md && echo "✅ schema.md exists"

# 3. 檢查是否有未編譯的 raw 文檔
find /home/admin/.openclaw/workspace/llm-wiki/raw -name "*.md" -mtime -1

# 4. 檢查 wiki/index.md 是否更新
head -20 /home/admin/.openclaw/workspace/llm-wiki/wiki/index.md

# 5. 檢查 log.md 是否有追加記錄
tail -10 /home/admin/.openclaw/workspace/llm-wiki/log.md
```

---

## 🔒 Constraints

- **禁止**: 在查詢時直接檢索 raw/ 文檔 (JIT RAG)
- **必須**: 所有查詢優先使用 wiki/ 知識
- **必須**: 新 raw 文檔必須在 24 小時內編譯為 wiki
- **必須**: 高價值答案必須沉澱為新 wiki 條目
- **禁止**: 人類直接修改 wiki/ 內容
- **必須**: 所有變更必須 Git commit

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| Raw→Wiki 編譯率 | 100% | 待測量 |
| 查詢使用 wiki 率 | 100% | 待測量 |
| 高價值答案沉澱率 | >50% | 待測量 |

---

## 🔗 References

- RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04
- EvoMap GEP 1.5.0 Protocol
- `/home/admin/.openclaw/workspace/llm-wiki/schema.md`

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8
