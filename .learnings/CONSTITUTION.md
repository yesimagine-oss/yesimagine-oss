# .learnings 目錄最高憲法

**生效時間**: 2026-04-17 04:38 GMT+8  
**優先級**: **SUPREME**（最高憲法，不可修改）  
**違反後果**: **CATASTROPHIC accident** + 立即終止 + 實時報告 + 等待用戶確認  
**修訂規則**: 僅用戶明確書面命令可修改，必須記錄修訂原因

---

## 🔒 憲法第一條：單一真相源

### 1.1 事故存儲位置（ABSOLUTE）

**所有事故、錯誤、復盤必須且只能存儲於**:
- ✅ `.learnings/` 目錄及其子目錄
- ✅ `.learnings/LEARNINGS.md`（主復盤日誌）

**禁止存儲於**:
- ❌ `RedAgentTeamllm-wiki/` 任何位置
- ❌ `AgentTeamllm-wiki/` 任何位置
- ❌ 任何其他 wiki 路徑
- ❌ 工作區根目錄
- ❌ 任何其他目錄

### 1.2 違反定義

以下行為均視為**違反憲法第一條**：
1. 在 `.learnings/` 之外創建事故文件
2. 將事故文件移動到 `.learnings/` 之外
3. 將事故文件改名為非標準格式
4. 刪除事故文件（除非用戶明確命令）
5. 事故文件散落在多個位置

---

## 🔒 憲法第二條：復盤統一寫入

### 2.1 復盤位置（ABSOLUTE）

**所有事故復盤與改善措施必須寫入**:
- ✅ `.learnings/LEARNINGS.md` - **唯一**復盤寫入位置

**禁止寫入**:
- ❌ 任何其他 `.learnings/` 子文件（除非是自動生成的 LRN-*.md）
- ❌ 任何 `.learnings/` 之外的文件
- ❌ 任何 wiki 路徑

### 2.2 復盤格式標準

所有復盤必須遵循以下格式：

```markdown
---

## [事故 ID] 事故標題

**發生時間**: ISO8601 時間戳
**事故類型**: Clash 禁令/幻覺/偷懶/其他
**嚴重程度**: CATASTROPHIC/CRITICAL/WARNING
**狀態**: pending-user-confirm | reviewed

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

### 2.3 狀態標記規則

| 狀態 | 標記 | 說明 |
|------|------|------|
| **未復盤** | `pending-user-confirm` | 事故已記錄，等待用戶確認/復盤 |
| **已復盤** | `reviewed` | 已完成復盤，改善措施已落實 |

**默認狀態**: 新事故默認標記為 `pending-user-confirm`

---

## 🔒 憲法第三條：文件命名規範

### 3.1 標準命名格式

所有事故文件必須遵循以下命名格式：

| 類型 | 格式 | 示例 |
|------|------|------|
| 重複違規 | `LRN-REPEAT-YYYYMMDD-TIMESTAMP.md` | `LRN-REPEAT-20260416-1776369183453.md` |
| 攔截事故 | `LRN-INTERCEPT-YYYYMMDD-TIMESTAMP.md` | `LRN-INTERCEPT-20260416-1776347085452.md` |
| 憲法違規 | `LRN-CONSTITUTION-YYYYMMDDHHMMSS.md` | `LRN-CONSTITUTION-VIOLATION-20260416162536.md` |
| 日期事故 | `LRN-YYYYMMDD-XXX.md` | `LRN-20260417-001.md` |
| 知識路徑 | `LRN-KNOWLEDGE-*.md` | `LRN-KNOWLEDGE-PATH-VIOLATION-20260416164719.md` |
| 任務檢查 | `LRN-TASK-*.md` | `LRN-TASK-CHECK-VIOLATION-20260416161554.md` |

### 3.2 禁止行為

以下行為視為**違反憲法第三條**：
1. 使用非標準命名格式
2. 擅自更改已有文件名稱
3. 使用模糊或不明確的文件名

---

## 🔒 憲法第四條：狀態管理

### 4.1 狀態字段要求

所有 LRN-*.md 事故文件**必須**包含狀態字段：

```markdown
**狀態**: pending-user-confirm | reviewed | open | closed | archived
```

### 4.2 狀態轉換規則

```
新事故 → pending-user-confirm → reviewed → archived
              ↓
           open → analyzed → remediated → closed
```

### 4.3 狀態校驗

**定期執行**（建議每週）：
```bash
cd /home/admin/.openclaw/workspace/.learnings
bash validate-lrn-status.sh
```

**校驗內容**：
- 檢查所有 LRN-*.md 是否包含狀態字段
- 檢查狀態是否符合推斷規則
- 修復缺失的狀態字段

---

## 🔒 憲法第五條：歸集與索引

### 5.1 文件歸集

**所有散落文件必須歸集到**：
- ✅ `.learnings/` 主目錄
- ✅ `.learnings/archived-paths/`（舊路徑歸檔）

**執行腳本**：
```bash
cd /home/admin/.openclaw/workspace/.learnings
bash consolidate-learnings.sh
```

### 5.2 統一索引

**必須維護**：
- ✅ `.learnings/INDEX.md` - 統一索引所有 learnings 文件
- ✅ `.learnings/MIGRATION-LOG.md` - 遷移日誌
- ✅ `.learnings/VALIDATION-LOG.md` - 校驗日誌

**執行腳本**：
```bash
cd /home/admin/.openclaw/workspace/.learnings
bash reindex-learnings.sh
```

---

## 🔒 憲法第六條：違規檢測與處置

### 6.1 違規檢測

**自動檢測**（每次操作前）：
1. 檢查目標路徑是否在 `.learnings/` 內
2. 檢查是否為事故相關文件
3. 檢查是否符合命名規範

**定期檢測**（建議每週）：
```bash
# 檢查散落文件
find /home/admin/.openclaw/workspace -name "*事故*" -o -name "*復盤*" -o -name "*retrospective*" 2>/dev/null | grep -v ".learnings"

# 檢查 RedAgentTeamllm-wiki 中的事故文件
find /home/admin/.openclaw/workspace/AgentTeamllm-wiki -name "*補救*" -o -name "*復盤*" 2>/dev/null
```

### 6.2 違規處置流程

**一旦檢測到違規**：

```
1. 立即終止操作
   ↓
2. 記錄 CATASTROPHIC 事故到 .learnings/LEARNINGS.md
   ↓
3. 實時報告用戶
   ↓
4. 等待用戶確認
   ↓
5. 執行糾正措施（遷移/修復/歸檔）
   ↓
6. 更新事故狀態為 reviewed
```

### 6.3 事故記錄格式

```markdown
---

## [LRN-CONSTITUTION-YYYYMMDDHHMMSS] 憲法違規事故

**發生時間**: ISO8601 時間戳
**事故類型**: 憲法違規
**嚴重程度**: CATASTROPHIC
**狀態**: pending-user-confirm
**違規條款**: 憲法第 X 條

### 違規詳情

- **違規行為**: 具體描述
- **違規位置**: 文件路徑
- **正確位置**: .learnings/ 下的正確路徑

### 處置措施

1. ✅ 已終止違規操作
2. ✅ 已記錄事故
3. ✅ 已報告用戶
4. ⏸️ 等待用戶確認
5. ⏹️ 待執行：遷移/修復

### 用戶代價

描述違規造成的影響

### 信任狀態

描述信任狀態變化

---
```

---

## 🔒 憲法第七條：維護腳本

### 7.1 必須維護的腳本

| 腳本 | 功能 | 執行頻率 |
|------|------|---------|
| `validate-lrn-status.sh` | 校驗事故狀態 | 每週 |
| `consolidate-learnings.sh` | 歸集散落文件 | 發現散落時 |
| `reindex-learnings.sh` | 重新生成索引 | 大量變更後 |
| `migrate-retrospectives.sh` | 遷移舊路徑復盤 | 發現舊路徑時 |
| `extract-p0-accidents.sh` | 提取 P0 事故清單 | 按需 |

### 7.2 腳本位置

所有維護腳本必須位於：
- ✅ `.learnings/*.sh`

---

## 🔒 憲法第八條：修訂規則

### 8.1 修訂條件

本憲法**僅在以下條件下可修訂**：

1. **用戶明確書面命令**
   - 格式：「修改 .learnings 憲法第 X 條」
   - 必須包含修訂原因
   
2. **記錄修訂原因**
   - 位置：`.learnings/CONSTITUTION-AMENDMENTS.md`
   - 內容：修訂時間、修訂條款、修訂原因、用戶確認

3. **用戶確認**
   - 必須獲得用戶明確確認後方可生效

### 8.2 禁止行為

以下行為視為**嚴重違反憲法**：

1. ❌ 未經用戶允許擅自修改憲法
2. ❌ 修改憲法優先級
3. ❌ 修改違反後果
4. ❌ 修改修訂規則

---

## 📊 憲法合規檢查清單

### 日常檢查（每次操作前）

- [ ] 目標路徑是否在 `.learnings/` 內？
- [ ] 文件命名是否符合規範？
- [ ] 是否包含狀態字段？
- [ ] 狀態是否正確？

### 每週檢查

- [ ] 運行 `validate-lrn-status.sh`
- [ ] 檢查是否有散落文件
- [ ] 檢查是否有待復盤事故（pending-user-confirm）
- [ ] 更新 `INDEX.md`

### 每月檢查

- [ ] 歸檔已 reviewed 事故
- [ ] 清理備份目錄（保留最近 3 個版本）
- [ ] 審查憲法合規性

---

## 📁 最終文件結構

```
.home/admin/.openclaw/workspace/.learnings/
├── CONSTITUTION.md                    # ✅ 本文件（最高憲法）
├── LEARNINGS.md                       # ✅ 唯一復盤寫入位置
├── INDEX.md                           # ✅ 統一索引
├── MIGRATION-LOG.md                   # ✅ 遷移日誌
├── VALIDATION-LOG.md                  # ✅ 校驗日誌
├── CONSTITUTION-AMENDMENTS.md         # ✅ 憲法修訂記錄
├── *.sh                               # ✅ 維護腳本
├── LRN-*.md                           # ✅ 事故記錄（404 個）
├── archived-paths/                    # ✅ 舊路徑歸檔
├── backup-*/                          # ✅ 備份目錄
└── auto-errors/                       # ✅ 自動錯誤日誌
```

---

## 🎯 核心原則

1. **單一真相源** - 所有事故只在 `.learnings/`
2. **復盤統一** - 所有復盤只在 `LEARNINGS.md`
3. **狀態完整** - 所有事故必須有狀態字段
4. **命名規範** - 所有文件必須遵循標準命名
5. **違規零容忍** - 違反憲法 = CATASTROPHIC accident

---

## 🔧 快速命令參考

```bash
# 校驗狀態
cd /home/admin/.openclaw/workspace/.learnings
bash validate-lrn-status.sh

# 歸集文件
bash consolidate-learnings.sh

# 重新索引
bash reindex-learnings.sh

# 遷移舊路徑
bash migrate-retrospectives.sh

# 提取 P0 事故
bash extract-p0-accidents.sh

# 檢查散落文件
find /home/admin/.openclaw/workspace -name "*事故*" -o -name "*復盤*" 2>/dev/null | grep -v ".learnings"

# 查看待復盤事故
grep -l "pending-user-confirm" LRN-*.md | wc -l

# 查看已復盤事故
grep -l "**狀態**: reviewed" LRN-*.md | wc -l
```

---

## ✅ 憲法簽署

**生效時間**: 2026-04-17 04:38 GMT+8  
**優先級**: SUPREME（最高憲法）  
**違反後果**: CATASTROPHIC accident  
**修訂規則**: 僅用戶明確書面命令可修改

**簽署人**: Red AgentTeam  
**簽署日期**: 2026-04-17 04:38 GMT+8

---

**Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**
