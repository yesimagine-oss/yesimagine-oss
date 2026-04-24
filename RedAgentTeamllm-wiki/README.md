# RedAgentTeamllm-wiki - 唯一指定知識庫

**狀態:** ✅ 生效中  
**最後更新:** 2026-04-24  
**路徑:** `/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/`  
**優先級:** 最高（所有回答前必查）

---

## 📁 目錄結構（科學分類）

```
RedAgentTeamllm-wiki/
├── 00-core/           # 核心配置、SOP、協議、規則
├── 01-openclaw/       # OpenClaw 平台（Gateway、配置、故障排除）
├── 02-evomap/         # EvoMap 相關（資產、任務、協議）
├── 03-projects/       # 項目知識（Node.js、Python、Serper、變現）
├── 04-skills/         # 技能與工具（API、腳本、集成）
├── 05-accidents/      # 事故記錄（P0/P1 事故、學習）
├── 06-reports/        # 報告（週報、月報、專項報告）
├── 07-learnings/      # 學習記錄（SOP、Gene、改進）
├── 08-genes/          # Gene 資產（可執行規則）
├── 09-capsules/       # Capsule 資產（實例膠囊）
├── 10-raw/            # 原始素材（未處理）
├── 11-archive/        # 歸檔（歷史文件）
├── scripts/           # 自動化腳本
├── logs/              # 日誌文件
└── backup/            # 備份
```

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
grep -ri "關鍵詞" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/00-core/ --include="*.md"

# 搜索事故
grep -ri "關鍵詞" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/05-accidents/ --include="*.md"

# 搜索學習
grep -ri "關鍵詞" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/07-learnings/ --include="*.md"

# 全局搜索
grep -ri "關鍵詞" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/ --include="*.md"
```

---

## 📋 使用原則

| 原則 | 說明 |
|------|------|
| **知識庫優先** | 回答前必須先搜索知識庫 |
| **沒有再外部** | 知識庫沒有，再查官方文檔 |
| **外部需確認** | 外部搜索需用戶同意 |
| **找到要引用** | 引用知識庫內容需註明來源 |
| **新知識要記錄** | 新發現要寫入知識庫 |

---

## 🚨 違反後果

**未經知識庫檢索就回答 = 系統錯誤**

必須：
1. 承認錯誤
2. 立即搜索知識庫
3. 補充正確答案
4. 記錄到 `07-learnings/`

---

## 📝 記錄新知識

發現新知識時：

1. **判斷類型**
   - SOP/協議 → `00-core/`
   - OpenClaw → `01-openclaw/`
   - EvoMap → `02-evomap/`
   - 項目 → `03-projects/`
   - 事故 → `05-accidents/`
   - 報告 → `06-reports/`
   - 學習 → `07-learnings/`

2. **創建文件**
   ```bash
   echo "# 標題" > 07-learnings/YYYY-MM-DD-主題.md
   ```

3. **Git 提交**
   ```bash
   git add .
   git commit -m "新增：主題"
   ```

---

## 🔗 相關文件

| 文件 | 說明 |
|------|------|
| `.startup.md` | 啟動鉤子（包含知識庫路徑） |
| `AGENTS.md` | 會話啟動流程 |
| `PROTOCOLS.md` | 知識庫優先原則 |

---

## 📊 統計

| 指標 | 數值 |
|------|------|
| **文件總數** | ~3,634 |
| **目錄總數** | ~1,300 |
| **一級分類** | 14 個 |
| **總大小** | ~216MB |

---

**最後更新:** 2026-04-24  
**狀態:** ✅ 生效中  
**維護者:** Red Agent Team
