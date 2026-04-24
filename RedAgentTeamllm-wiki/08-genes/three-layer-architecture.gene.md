# Gene: Three Layer Architecture

**gene_id**: `GENE_002_THREE_LAYER_ARCHITECTURE`  
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

Three immutable layers: Raw (source of truth, read-only), Wiki (LLM-owned structured markdown), Schema (workflow specification).

三層不可變架構：Raw (真相來源，只讀), Wiki (LLM 所有的結構化 Markdown), Schema (工作流規範)。

---

## 🎯 Content

**三層架構定義**:

### 第一層：Raw (原始資料層)

- **所有者**: 人類
- **權限**: 人類可寫，LLM 只讀
- **內容**: 原始文檔、源代碼、參考資料
- **特點**: 是真相來源 (source of truth)，不可由 LLM 修改
- **位置**: `llm-wiki/raw/`

### 第二層：Wiki (編譯知識層)

- **所有者**: LLM
- **權限**: LLM 可寫，人類只讀
- **內容**: 結構化知識條目、索引、摘要
- **特點**: 由 LLM 維護，持續更新，結構化組織
- **位置**: `llm-wiki/wiki/`

### 第三層：Schema (規範層)

- **所有者**: 人類 + LLM 共同
- **權限**: 需雙方審批
- **內容**: 工作流規範、職責分離、質量指標
- **特點**: 定義系統如何運作，協同進化
- **位置**: `llm-wiki/schema.md`

**為什麼是三層**:

1. **職責分離** - 人類控制輸入，LLM 負責維護
2. **真相單一** - Raw 是唯一真相來源，避免知識漂移
3. **結構清晰** - 每層有明確目的和權限
4. **可審計** - 每層的變更都可追蹤

**與 Genes/Capsules 的關係**:

- Genes 存儲在 `genes/`，屬於 Schema 層的擴展
- Capsules 存儲在 `capsules/`，是具體實現
- Genes 定義規則，Capsules 執行規則

---

## 🧬 Signals

`three_layer`, `architecture`, `Raw`, `Wiki`, `Schema`, `separation_of_duty`, `source_of_truth`, `LLM_owned`, `human_owned`, `immutable`

---

## 📋 Strategy

### 步驟 1: 創建目錄結構
建立 `raw/`, `wiki/`, `genes/`, `capsules/` 四個核心目錄。

### 步驟 2: 定義權限邊界
在 schema.md 中明確每層的所有者和權限。

### 步驟 3: 遷移現有文件
將現有文件分類到對應層級。

### 步驟 4: 建立保護機制
確保 LLM 不修改 raw/，人類不修改 wiki/。

### 步驟 5: 文檔化架構
在 schema.md 中完整記錄三層架構設計。

---

## ✅ Validation

```bash
# 1. 檢查目錄結構
ls -la /home/admin/.openclaw/workspace/llm-wiki/ | grep -E "raw|wiki|genes|capsules"

# 2. 檢查 Raw 層
ls /home/admin/.openclaw/workspace/llm-wiki/raw/ | head -10

# 3. 檢查 Wiki 層
ls /home/admin/.openclaw/workspace/llm-wiki/wiki/ | head -10

# 4. 檢查 Schema 文件
cat /home/admin/.openclaw/workspace/llm-wiki/schema.md | head -30

# 5. 檢查權限 (可選)
stat /home/admin/.openclaw/workspace/llm-wiki/raw/ /home/admin/.openclaw/workspace/llm-wiki/wiki/
```

---

## 🔒 Constraints

- **禁止**: LLM 修改 raw/ 中的任何文件
- **禁止**: 人類直接修改 wiki/ 中的任何文件
- **必須**: 所有新文件必須放入正確層級
- **必須**: Raw→Wiki 的編譯必須保留來源引用
- **必須**: Schema 變更必須雙方同意
- **禁止**: 跨層級直接引用 (必須通過索引)

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| 目錄結構完整率 | 100% | 100% ✅ |
| 權限邊界遵守率 | 100% | 待監測 |
| 文件分類正確率 | 100% | 待測量 |

---

## 🔗 References

- RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04
- `/home/admin/.openclaw/workspace/llm-wiki/schema.md`
- `GENE_001_REDAGENTTEAMLLM-WIKI_CORE_IDEAL`

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8
