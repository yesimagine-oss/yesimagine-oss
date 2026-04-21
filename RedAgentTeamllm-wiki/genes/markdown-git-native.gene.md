# Gene: Markdown Git Native

**gene_id**: `GENE_007_MARKDOWN_GIT_NATIVE`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04  
**category**: 技術棧  
**risk_level**: low  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T05:45:00Z

---

## 📝 Summary

Wiki is pure markdown + git; versioned, branchable, no heavy database; compatible with Obsidian.

知識庫是純 Markdown + Git；可版本控制、可分支、無重型數據庫；與 Obsidian 兼容。

---

## 🎯 Content

**Markdown + Git -native 定義**:

知識庫使用純文本 Markdown 格式，由 Git 進行版本控制，不使用重型數據庫。

### 為什麼選擇 Markdown?

#### 優點
- **人類可讀** - 純文本，無需特殊工具即可閱讀
- **簡單** - 語法簡單，易學易用
- **通用** - 幾乎所有編輯器都支持
- **輕量** - 文件小，加載快
- **持久** - 不依賴特定軟件格式
- **可版本控制** - Git 友好，diff 清晰

#### 與 HTML 對比
- Markdown 更簡潔
- 專注內容而非展示
- 更易於 LLM 生成和解析

### 為什麼選擇 Git?

#### 優點
- **版本歷史** - 所有變更可追溯
- **分支實驗** - 可創建實驗分支
- **合併跟蹤** - 自動記錄合併歷史
- **分布式** - 本地也有完整歷史
- **工具生態** - 豐富的 Git 工具鏈
- **備份** - 多副本天然備份

#### 與數據庫對比
- 無須數據庫服務
- 無須備份策略 (Git 即備份)
- 無性能瓶頸 (文本文件)
- 更易審計

### Obsidian 兼容性

Obsidian 是流行的 Markdown 知識庫工具:

- **雙向鏈接** - `[[頁面名]]` 語法
- **知識圖譜** - 可視化引用關係
- **本地優先** - 文件在本地
- **Git 集成** - 可使用 Git 備份
- **插件生態** - 豐富的功能擴展

**我們的實現**:

- ✅ 所有 wiki 條目為 `.md` 文件
- ✅ 使用 Git 版本控制
- ✅ 支持 Obsidian 打開
- ✅ 無數據庫依賴
- ✅ 純文本存儲

**最佳實踐**:

1. **文件命名** - 使用小寫 + 連字符 (`docker-layer-cache.md`)
2. **標題格式** - 每個文件以 `# 標題` 開頭
3. **內部鏈接** - 使用 `[文字](文件.md)` 或 `[[文件]]`
4. **提交信息** - 清晰的提交信息 (`feat: 添加 Docker 優化指南`)
5. **分支策略** - main 為生產，feature 分支用於實驗

---

## 🧬 Signals

`markdown`, `git`, `version_control`, `no_database`, `plain_text`, `Obsidian_compatible`, `branchable`, `auditable`, `lightweight`, `persistent`

---

## 📋 Strategy

### 步驟 1: 確保所有文件為 Markdown
檢查 llm-wiki/ 中所有文檔是否為 .md 格式。

### 步驟 2: 初始化 Git 倉庫
如未初始化，執行 `git init`。

### 步驟 3: 配置 Git 用戶
設置 LLM 的 Git 用戶信息。

### 步驟 4: 建立提交規範
定義提交信息格式和頻率。

### 步驟 5: 測試 Obsidian 兼容
用 Obsidian 打開知識庫驗證。

---

## ✅ Validation

```bash
# 1. 檢查是否為 Git 倉庫
cd /home/admin/.openclaw/workspace && git status

# 2. 檢查 Markdown 文件比例
find /home/admin/.openclaw/workspace/llm-wiki -name "*.md" | wc -l
find /home/admin/.openclaw/workspace/llm-wiki -type f | wc -l

# 3. 檢查 Git 提交歷史
cd /home/admin/.openclaw/workspace && git log --oneline -10 -- llm-wiki/

# 4. 檢查是否有非 Markdown 文件
find /home/admin/.openclaw/workspace/llm-wiki -type f ! -name "*.md" ! -name ".gitignore"

# 5. 測試 Obsidian 兼容性 (手動)
# 用 Obsidian 打開 llm-wiki 目錄，檢查鏈接是否正常
```

---

## 🔒 Constraints

- **必須**: 所有知識條目為 Markdown 格式
- **必須**: 使用 Git 版本控制
- **必須**: 每次變更必須 Git commit
- **禁止**: 使用數據庫存儲知識
- **禁止**: 使用二進制格式 (PDF 等除外)
- **必須**: 提交信息清晰描述變更
- **必須**: 支持 Obsidian 打開

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| Markdown 文件比例 | 100% | 待測量 |
| Git 提交覆蓋率 | 100% | 待測量 |
| Obsidian 兼容率 | 100% | 待驗證 |
| 平均提交頻率 | ≥1 次/天 | 待測量 |
| 提交信息質量 | 主觀評估 | 待評估 |

---

## 🔗 References

- RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04
- Obsidian: https://obsidian.md
- Git: https://git-scm.com
- `/home/admin/.openclaw/workspace/llm-wiki/`

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8
