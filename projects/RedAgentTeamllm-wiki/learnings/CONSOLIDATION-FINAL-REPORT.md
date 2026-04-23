# Gene 正式入庫查重合併報告

**生成時間**: 2026-04-17 08:52 GMT+8  
**執行路徑**: `RedAgentTeamllm-wiki/learnings/`  
**狀態**: ✅ 完成，等待用戶確認

---

## 📊 統計摘要

| 指標 | 數值 |
|------|------|
| **原始 Gene 數量** | 468 |
| **重複集群數量** | 27 |
| **合併後 Gene 數量** | 49 |
| **減少數量** | 419 |
| **壓縮率** | 89.5% |

---

## 🔍 查重結果

### 相似度閾值
- **Signals 重疊率 + Strategy 相似度** > 80% → 判定為重複

### 主要重複集群

| 集群 ID | 重複文件數 | 合併後 Signals | 說明 |
|---------|-----------|-------------|------|
| 1 | 171 | 175 | GENE-INTERCEPT 系列（最大集群） |
| 3 | 153 | 157 | GENE-INTERCEPT 系列（第二集群） |
| 5 | 8 | 12 | GENE-REPEAT 系列 |
| 6 | 8 | 12 | GENE-REPEAT 系列 |
| 13 | 9 | 13 | GENE-REPEAT 系列 |
| 其他 22 個集群 | 2-7 | 6-11 | 各類重複 Gene |

---

## 📁 輸出文件

### 合併目錄
```
RedAgentTeamllm-wiki/learnings/merged/
├── GENE-MERGED-001.md ~ GENE-MERGED-027.md  (27 個合併後 Gene)
├── GENE-20260416-*.md  (6 個未合併 Gene)
├── GENE-20260417-*.md  (10 個未合併 Gene)
├── GENE-REPEAT-*.md    (6 個未合併 Gene)
├── GENE-*.md           (其他未合併 Gene)
├── MERGE-REPORT.md     (詳細合併報告)
└── MERGE-REPORT.json   (機器可讀報告)
```

### 報告文件
- **詳細報告**: `RedAgentTeamllm-wiki/learnings/merged/MERGE-REPORT.md`
- **JSON 報告**: `RedAgentTeamllm-wiki/learnings/merged/MERGE-REPORT.json`
- **腳本**: 
  - `dedup_genes.py` (查重腳本)
  - `merge_genes.py` (合併腳本)

---

## ✅ 合併處理

### 合併策略
1. **Signals 合併**: 所有重複 Gene 的 Signals 去重後合併
2. **Strategy 合併**: 保留最完整的 Strategy 版本
3. **References 添加**: 列出所有被合併的原始 Gene 文件名
4. **Root Cause 合併**: 合併不同的根本原因（最多 3 個）
5. **Consequences 合併**: 合併不同的後果描述（最多 3 個）

### 合併示例
```markdown
# Gene: gene_accident_xxx

**合併狀態**: ✅ 已合併 171 個重複 Gene

## 參考文獻 (References)
本 Gene 由以下 171 個重複 Gene 合併而成：
1. GENE-INTERCEPT-20260416-1776347145833.md
2. GENE-INTERCEPT-20260416-1776347085443.md
...
```

---

## ⚠️ 用戶確認事項

### 請確認以下內容：

1. **查重結果是否合理？**
   - 27 個集群，468 → 49 個 Gene
   - 壓縮率 89.5%

2. **合併策略是否正確？**
   - Signals 去重合併
   - Strategy 保留最完整版本
   - References 完整記錄

3. **是否可以正式入庫？**
   - 確認後可將 `merged/` 目錄內容移至正式庫
   - 或需要進一步調整？

---

## 📋 後續步驟

### 選項 A: 確認入庫
```bash
# 將合併後的 Gene 移至正式庫
mv RedAgentTeamllm-wiki/learnings/merged/GENE-*.md RedAgentTeamllm-wiki/learnings/
# 備份原始文件
mkdir -p RedAgentTeamllm-wiki/learnings/backup-raw
mv RedAgentTeamllm-wiki/learnings/GENE-*.md RedAgentTeamllm-wiki/learnings/backup-raw/
```

### 選項 B: 進一步審查
- 查看 `merged/MERGE-REPORT.md` 詳細報告
- 抽查合併後的 Gene 文件質量
- 調整合併策略後重新執行

### 選項 C: 取消操作
- 保留 `merged/` 目錄作為參考
- 不進行任何移動操作

---

## 🎯 完成狀態

✅ **已生成 Gene，查重結果 27 個集群（468 → 49），請確認**

---

*報告生成：Red Agent Team｜🦞RedOpenClaw*  
*時間：2026-04-17 08:52 GMT+8*
