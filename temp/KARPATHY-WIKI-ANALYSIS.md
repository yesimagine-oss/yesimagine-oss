# Karpathy LLM Wiki 架構分析報告

**分析時間**: 2026-04-17 05:45 GMT+8  
**來源**: 用戶提供的 Karpathy LLM Wiki Original 2026-04-04

---

## 📊 架構對比

| 層面 | Karpathy 標準架構 | 我們現狀 | 差異 |
|------|------------------|----------|------|
| **根目錄** | `/home/admin/AgentTeamllm-wiki/` | `/home/admin/.openclaw/workspace/llm-wiki/` | ✅ 路徑不同但結構相似 |
| **Raw 層** | `raw/` (不可變，只讀) | `raw/` + `raw/raw/` | ⚠️ 我們有嵌套，略顯混亂 |
| **Wiki 層** | `wiki/` (LLM 維護) | `wiki/` | ✅ 一致 |
| **Schema** | `schema.md` (核心規範) | ❌ 缺失 | 🔴 **關鍵缺失** |
| **Genes** | `genes/` (規則基因) | ❌ 無獨立目錄 | 🔴 **缺失** |
| **Capsules** | `capsules/` (實例膠囊) | `ollama/capsules/` (僅 Ollama) | ⚠️ 部分實現 |
| **Log** | `log.md` (追加式) | `log.md` + 多個 log.md | ⚠️ 分散 |
| **Index** | `index.md` | `index.md` + 多個 INDEX.md | ⚠️ 分散 |

---

## 🧬 Karpathy 8 個核心 Genes

| Gene ID | 名稱 | 我們是否有 | 狀態 |
|---------|------|-----------|------|
| GENE_001 | KARPATHY_CORE_IDEAL (AOT 編譯) | ❌ 無 | 需導入 |
| GENE_002 | THREE_LAYER_ARCHITECTURE | 🟡 部分 (raw/wiki) | 需補全 schema |
| GENE_003 | INGEST_WORKFLOW | ❌ 無明確定義 | 需導入 |
| GENE_004 | QUERY_WORKFLOW | 🟡 隱式存在 | 需形式化 |
| GENE_005 | LINT_WORKFLOW | ✅ 有 lint-report | 需系統化 |
| GENE_006 | HUMAN_LLM_DUTY_SEPARATION | 🟡 隱式遵守 | 需明確規定 |
| GENE_007 | MARKDOWN_GIT_NATIVE | ✅ 完全符合 | 已實現 |
| GENE_008 | SCHEMA_CO_EVOLUTION | ❌ 無 schema.md | 需創建 |

---

## 📦 Karpathy 8 個 Capsules

| Capsule ID | 對應 Gene | 我們是否有 | 狀態 |
|-----------|----------|-----------|------|
| CAPSULE_001 | CORE_IDEAL | ❌ | 需實現 |
| CAPSULE_002 | THREE_LAYER_INIT | 🟡 部分 | 需補全 |
| CAPSULE_003 | INGEST_EXECUTOR | ❌ | 需實現 |
| CAPSULE_004 | QUERY_ENGINE | 🟡 部分 | 需增強 |
| CAPSULE_005 | LINT_INSPECTOR | 🟡 有報告 | 需自動化 |
| CAPSULE_006 | ORCHESTRATOR | ❌ | 需實現 |
| CAPSULE_007 | GIT_MARKDOWN_BACKEND | ✅ | 已實現 |
| CAPSULE_008 | SCHEMA_COEVOLVE | ❌ | 需創建 |

---

## ✅ 我們做得好的地方

| 優勢 | 說明 |
|------|------|
| **Markdown + Git** | 完全符合 Karpathy 理念 |
| **Raw/Wiki 分離** | 三層架構已實現兩層 |
| **Log 機制** | 有日志記錄傳統 |
| **Index 索引** | 有總索引文件 |
| **Ollama 資產包** | 已實現 Gene/Capsule 分離 (EvoMap 標準) |

---

## 🔴 我們的不足

| 不足 | 影響 | 優先級 |
|------|------|--------|
| **缺少 schema.md** | 無明確工作流規範 | P0 |
| **缺少 genes/ 目錄** | 規則基因散落各處 | P0 |
| **缺少 capsules/ 目錄** | 僅 Ollama 有，無統一位置 | P1 |
| **多個 log.md 分散** | 日志不集中，難追蹤 | P1 |
| **多個 index.md 分散** | 索引不統一 | P1 |
| **無 AOT 編譯理念** | 可能仍有 JIT RAG 問題 | P0 |
| **無 Lint 自動化** | 只有報告，無自動修復 | P2 |
| **無 Human/LLM 職責分離文檔** | 邊界模糊 | P1 |

---

## 🎯 建議改進措施

### 短期 (P0 - 立即執行)

1. **創建 `schema.md`** - 定義核心工作流規範
2. **創建 `genes/` 目錄** - 遷入 Karpathy 8 Genes + 現有規則
3. **創建 `capsules/` 目錄** - 統一膠囊存放位置
4. **導入 AOT 編譯理念** - 明確禁止 JIT RAG

### 中期 (P1 - 1 周內)

5. **統一 log.md** - 合併所有分散日志到單一文件
6. **統一 index.md** - 創建單一權威索引
7. **明確 Human/LLM 職責** - 文檔化邊界
8. **遷移 Ollama 資產** - 將 `ollama/genes/` 遷入統一 `genes/`

### 長期 (P2 - 持續改進)

9. **實現 Lint 自動化** - 自動檢測並修復問題
10. **實現 Ingest 工作流** - 自動化知識編譯
11. **實現 Query 工作流** - 自動保存高價值答案

---

## 📋 執行建議

**是否現在執行？**

建議立即執行 P0 措施 (1-4)，因為：
- 不破壞現有結構
- 補充缺失的核心規範
- 為未來擴展奠定基礎

**執行順序**:
```bash
# 1. 創建 schema.md
# 2. 創建 genes/ 目錄
# 3. 創建 capsules/ 目錄  
# 4. 遷入 Karpathy 8 Genes
# 5. 遷入 Ollama 17 Genes + 7 Capsules
# 6. 更新 index.md 和 log.md
```

---

## 🤔 是否吸取 Karpathy 架構？

**✅ 強烈建議吸取**

**理由**:
1. **經過驗證** - Karpathy 原始設計，理念成熟
2. **與我們兼容** - Markdown + Git 完全一致
3. **補充缺失** - schema.md 是我們最缺的
4. **EvoMap 兼容** - Gene/Capsule 概念與 EvoMap GEP 1.5.0 完美契合
5. **不破壞現有** - 是補充，不是重構

**融合策略**:
```
Karpathy 架構 (宏觀) + EvoMap 標準 (微觀) = 我們的混合架構
```

---

**建議**: 立即執行 P0 措施，將 Karpathy 8 Genes 存入 `genes/`，創建 `schema.md`。
