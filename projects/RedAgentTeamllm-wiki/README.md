# RedAgentTeamllm-wiki - 唯一指定知識庫

**狀態:** ✅ 生效中  
**最後更新:** 2026-04-24  
**優先級:** 最高（所有回答前必查）

---

## 📍 路徑

```
/home/admin/.openclaw/workspace/projects/RedAgentTeamllm-wiki/
```

---

## 📁 結構

```
RedAgentTeamllm-wiki/
├── README.md              # 本文件（知識庫說明）
├── wiki/                  # 知識文檔
│   ├── serper/           # Serper API 相關
│   ├── evomap/           # EvoMap 相關
│   ├── learning/         # 學習筆記
│   ├── reports/          # 報告
│   └── ...               # 其他主題
├── reports/               # 所有報告
├── accidents/             # 事故記錄
├── learnings/             # 學習記錄
├── protocols/             # 協議文檔
├── logs/                  # 日誌
├── analysis/              # 分析報告
├── audit/                 # 審計記錄
├── backup/                # 備份
├── briefings/             # 簡報
├── capsules/              # Capsule 資產
├── deliberations/         # 審議記錄
├── genes/                 # Gene 資產
├── monetization/          # 變現相關
├── protocol/              # 協議
├── rules/                 # 規則
├── schema/                # 架構
├── scripts/               # 腳本
└── tasks/                 # 任務
```

---

## 🔍 檢索規則

### 回答問題前必須

1. **搜索 `wiki/`** — 知識文檔
2. **搜索 `reports/`** — 歷史報告
3. **搜索 `accidents/`** — 事故記錄
4. **搜索 `learnings/`** — 學習記錄

### 搜索命令

```bash
# 搜索關鍵詞
grep -ri "關鍵詞" /home/admin/.openclaw/workspace/projects/RedAgentTeamllm-wiki/ --include="*.md"

# 搜索特定主題
grep -ri "關鍵詞" /home/admin/.openclaw/workspace/projects/RedAgentTeamllm-wiki/wiki/ --include="*.md"

# 搜索報告
grep -ri "關鍵詞" /home/admin/.openclaw/workspace/projects/RedAgentTeamllm-wiki/reports/ --include="*.md"
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
4. 記錄到 `.learnings/`

---

## 📝 記錄新知識

發現新知識時：

1. **判斷類型**
   - 技術文檔 → `wiki/`
   - 報告 → `reports/`
   - 事故 → `accidents/`
   - 學習 → `learnings/`

2. **創建文件**
   ```bash
   # 格式：YYYY-MM-DD-主題.md
   echo "# 標題" > wiki/YYYY-MM-DD-主題.md
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

**最後更新:** 2026-04-24  
**狀態:** ✅ 生效中
