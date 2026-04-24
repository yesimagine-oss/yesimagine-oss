# RedAgentTeamllm-wiki 知識庫結構

**最後整理:** 2026-04-24 13:45  
**狀態:** ✅ 科學優化完成

---

## 📁 最終結構（13 個一級目錄）

```
RedAgentTeamllm-wiki/
├── 00-core/           # 核心協議/SOP/規則
├── 01-openclaw/       # OpenClaw 平台（Schema/Council/GDI/變現）
├── 02-evomap/         # EvoMap（16 個二級目錄，已科學整理）
├── 03-projects/       # 項目知識（Node.js/Python/Docker 等）
├── 04-skills/         # 技能與工具（API/腳本/集成）
├── 05-accidents/      # 事故記錄（P0/P1 事故）
├── 06-reports/        # 報告（週報/月報/專項）
├── 07-learnings/      # 學習記錄（SOP/Gene/改進）
├── 08-genes/          # Gene 資產（可執行規則）
├── 09-capsules/       # Capsule 資產（實例膠囊）
├── 10-raw/            # 原始素材（未處理）
├── 11-archive/        # 歸檔（歷史文件/代碼）
└── scripts/           # 自動化腳本
```

---

## 📊 優化成果

| 指標 | 優化前 | 優化後 | 改進 |
|------|--------|--------|------|
| **一級目錄** | 17 個 | 13 個 | -24% |
| **總目錄數** | 1,312 個 | 466 個 | -64% |
| **最深層級** | 10 層 | 8 層（已歸檔） | -20% |
| **活躍深度** | 7 層+ | ≤3 層 | -57% |
| **node_modules** | 多個 | 0 個 | ✅ 清除 |
| **重複目錄** | 4 組 | 0 組 | ✅ 清除 |

---

## 🎯 核心文檔位置

| 主題 | 位置 |
|------|------|
| **回復標準 SOP** | `00-core/回復標準-SOP（胡老師專用）.md` |
| **知識入庫 SOP** | `00-core/知識入庫回復標準-SOP.md` |
| **Schema 1.5.0** | `01-openclaw/schema-1.5.0.md` |
| **AI Council** | `01-openclaw/ai-council.md` |
| **GDI 優化** | `01-openclaw/gdi-optimization.md` |
| **變現渠道** | `01-openclaw/monetization.md` |
| **Token 消耗實測** | `00-core/知識入庫回復標準-SOP.md` |

---

## 🔍 檢索規則

### 回答問題前必須

1. **搜索 `00-core/`** — SOP、協議
2. **搜索 `05-accidents/`** — 事故記錄
3. **搜索 `07-learnings/`** — 學習記錄
4. **搜索相關主題目錄** — 01-04

### 搜索命令

```bash
# 搜索 SOP
grep -ri "關鍵詞" RedAgentTeamllm-wiki/00-core/ --include="*.md"

# 搜索事故
grep -ri "關鍵詞" RedAgentTeamllm-wiki/05-accidents/ --include="*.md"

# 全局搜索
grep -ri "關鍵詞" RedAgentTeamllm-wiki/ --include="*.md"
```

---

## ✅ 清理項目

| 項目 | 狀態 | 說明 |
|------|------|------|
| **node_modules** | ✅ 清除 | 所有依賴目錄已移除 |
| **src/ 代碼** | ✅ 清除 | 源代碼已移除 |
| **raw/ 重複** | ✅ 合併 | 空目錄已刪除 |
| **reports/ 重複** | ✅ 合併 | 併入 06-reports/ |
| **backup/ 重複** | ✅ 合併 | 併入 .backups/ |
| **logs/ 空目錄** | ✅ 清除 | 空目錄已刪除 |
| **agent-browser** | ✅ 歸檔 | 代碼歸檔到 11-archive/ |

---

## 📈 知識庫統計

| 指標 | 數值 |
|------|------|
| **Markdown 文件** | ~3,179 個 |
| **一級目錄** | 13 個 |
| **總目錄數** | 466 個 |
| **備份位置** | `.backups/` |
| **Git 提交** | 170+ 次 |

---

## 🚨 使用原則

| 原則 | 說明 |
|------|------|
| **知識庫優先** | 回答前必須先搜索知識庫 |
| **本地讀取** | ✅ 0 Token 消耗（實測驗證） |
| **沒有再外部** | 知識庫沒有，再查官方文檔 |
| **外部需確認** | 外部搜索需用戶同意 |
| **找到要引用** | 引用需註明來源文件 |

---

## 📝 備份位置

| 備份 | 位置 |
|------|------|
| **02-evomap 整理** | `.backups/2026-04-24-evomap-restructure/` |
| **Wiki 最終備份** | `.backups/2026-04-24-wiki-final/` |
| **Wiki 結構整理** | `.backups/2026-04-24-wiki-restructure/` |

---

**維護者:** Red Agent Team  
**下次審查:** 2026-05-01  
**版本:** v2.0（科學優化版）
