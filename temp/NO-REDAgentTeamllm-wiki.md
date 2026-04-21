# 禁止寫入 RedAgentTeamllm-wiki 聲明

**生效時間**: 2026-04-17 04:24 GMT+8  
**優先級**: HIGHEST（最高優先級，不可修改）  
**違反後果**: CRITICAL accident + 立即終止 + 實時報告

---

## 🔒 憲法鎖定：禁止寫入 RedAgentTeamllm-wiki

### 規則 1：事故復盤統一位置（ABSOLUTE）

**所有事故復盤與改善措施必須寫入**:
- ✅ `.learnings/LEARNINGS.md` - 唯一事故復盤位置
- ✅ `.learnings/` 目錄下的其他文件

**禁止寫入**:
- ❌ `RedAgentTeamllm-wiki/` 任何位置
- ❌ `AgentTeamllm-wiki/wiki/reports/` 
- ❌ `AgentTeamTeamllm-wiki/wiki/learning/`
- ❌ 任何其他 wiki 路徑

### 規則 2：現有文件遷移（ABSOLUTE）

**已遷移文件**:
| 原始路徑 | 遷移狀態 | 遷移時間 |
|---------|---------|---------|
| `AgentTeamllm-wiki/wiki/reports/RedAgentTeamllm-wiki-補救報告 -20260414.md` | ✅ 已遷移 | 2026-04-17 04:24 |
| `AgentTeamllm-wiki/wiki/reports/RedAgentTeamllm-wiki-規範整理報告 -20260414.md` | ✅ 已遷移 | 2026-04-17 04:24 |
| `AgentTeamllm-wiki/wiki/reports/RedAgentTeamllm-wiki-健康度報告 -20260414.md` | ✅ 已遷移 | 2026-04-17 04:24 |
| `AgentTeamllm-wiki/wiki/learning/task6-retrospective.md` | ✅ 已遷移 | 2026-04-17 04:24 |
| `AgentTeamllm-wiki/wiki/learning/high-value-asset-workflow-retrospective.md` | ✅ 已遷移 | 2026-04-17 04:24 |
| `AgentTeamllm-wiki/wiki/learning/old-node-25-assets-retrospective.md` | ✅ 已遷移 | 2026-04-17 04:24 |
| `AgentTeamllm-wiki/wiki/learning/dual-node-55-bundles-retrospective.md` | ✅ 已遷移 | 2026-04-17 04:24 |

**遷移目標**: `.learnings/LEARNINGS.md` - 「事故復盤與改善措施」章節

### 規則 3：新事故復盤流程（ABSOLUTE）

**當發生新事故時**:

1. **立即記錄** → `.learnings/LEARNINGS.md` 頂部「事故復盤與改善措施」章節
2. **格式要求**:
   ```markdown
   ---
   
   ## [事故 ID] 事故標題
   
   **發生時間**: ISO8601 時間戳
   **事故類型**: Clash 禁令/幻覺/偷懶/其他
   **嚴重程度**: CATASTROPHIC/CRITICAL/WARNING
   
   ### 事件經過
   
   簡短描述事件發生過程
   
   ### 根因分析
   
   分析事故根本原因
   
   ### 改善措施
   
   - [ ] 具體改善行動 1
   - [ ] 具體改善行動 2
   
   ### 教訓總結
   
   核心教訓和未來指導原則
   
   ---
   ```
3. **禁止操作** → 不得創建新的 RedAgentTeamllm-wiki 文件

### 規則 4：違規檢測（ABSOLUTE）

**當檢測到寫入 RedAgentTeamllm-wiki 時**:

1. **立即終止** 寫入操作
2. **記錄事故** → `.learnings/LEARNINGS.md`
3. **實時報告** → 向用戶報告違規
4. **等待指示** → 等待用戶確認後繼續

### 規則 5：定期檢查（ABSOLUTE）

**每週執行**:

```bash
# 檢查是否有新的 RedAgentTeamllm-wiki 事故文件
find AgentTeamllm-wiki -name "*補救*" -o -name "*復盤*" -o -name "*retrospective*" 2>/dev/null

# 如果發現 → 立即遷移並記錄
```

---

## 📊 遷移統計

| 指標 | 數值 |
|------|------|
| 遷移文件數 | 7 |
| 遷移時間 | 2026-04-17 04:24 GMT+8 |
| 遷移目標 | `.learnings/LEARNINGS.md` |
| 舊路徑狀態 | 保留作為歷史參考 |

---

## ✅ 最終文件結構

```
.home/admin/.openclaw/workspace/
├── .learnings/
│   ├── LEARNINGS.md                 # ✅ 唯一事故復盤位置
│   ├── INDEX.md                     # 統一索引
│   ├── MIGRATION-LOG.md             # 遷移日誌
│   └── NO-REDAgentTeamllm-wiki.md   # 本文件
├── AgentTeamllm-wiki/
│   └── wiki/
│       ├── reports/                 # ⚠️ 舊路徑（已遷移，保留參考）
│       └── learning/                # ⚠️ 舊路徑（已遷移，保留參考）
```

---

## 🎯 核心原則

1. **單一真相源** - 所有事故復盤只在 `.learnings/LEARNINGS.md`
2. **禁止分散** - 不允許寫入 RedAgentTeamllm-wiki
3. **立即遷移** - 發現散落文件立即遷移
4. **歷史保留** - 舊文件保留作為參考，不再更新

---

## 🔧 維護腳本

```bash
# 遷移散落文件
cd /home/admin/.openclaw/workspace/.learnings
bash migrate-retrospectives.sh

# 檢查是否有新散落文件
find ../AgentTeamllm-wiki -name "*補救*" -o -name "*復盤*" 2>/dev/null
```

---

**生效時間**: 2026-04-17 04:24 GMT+8  
**修訂規則**: 僅用戶明確書面命令可修改  
**違反後果**: CRITICAL accident

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
