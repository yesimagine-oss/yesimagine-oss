# P3 - Lint 審計計劃 (反知識壞死)

**執行時間**: 2026-04-13T06:26:00+08:00  
**chain_id**: `p3_lint_20260413_062600`  
**目標**: 識別並修剪邏輯矛盾、過時策略、壞死資產

---

## 審計範圍

### 核心配置文件 (8 個)
- [ ] bootstrap.md
- [ ] identity.md
- [ ] soul.md
- [ ] tools.md
- [ ] agents.md
- [ ] memory.md
- [ ] heartbeat.md
- [ ] user.md

### 協議文件 (7 個)
- [ ] protocol_startup.md
- [ ] automation.md
- [ ] gdi-calculator.md
- [ ] dashboard.md
- [ ] gdi-report-20260413.md
- [ ] p1-publish-plan.md
- [ ] p2-distillation-plan.md

### 學習記錄 (10 個)
- .learnings/*.md (10 個文件)

### 記憶文件
- memory/2026-04-13.md
- MEMORY.md

---

## 審計標準

### 1. 邏輯矛盾檢測
```
檢查項目:
- 配置衝突 (如：同時啟用和禁用同一功能)
- 協議矛盾 (如：不同文件定義不同的心跳間隔)
- 簽名不一致 (如：統一簽名出現變體)

閾值:
- 發現矛盾 → 創建 contradiction tag
- 觸發推演 → 決定保留哪個版本
```

### 2. 過時策略識別
```
檢查項目:
- 引用已棄用的 API
- 使用舊 schema_version (< 1.5.0)
- 提及不存在的功能

閾值:
- 過時 > 30 天 → 標記為 stale
- 過時 > 90 天 → 標記為 archived
```

### 3. 壞死資產修剪
```
GDI 標準:
- GDI < 40 (連續 3 次) → 降級為 stale
- 170 天未被 FETCH → 降級為 archived

當前狀態:
- 7 個資產 GDI 均為 40-69 (🟠 Review)
- 無需立即修剪
- 需要優化提升
```

---

## 審計流程

### 階段 1: 配置文件一致性檢查
```
1. 檢查 8 個核心配置文件的簽名一致性
   - 預期：RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...
   
2. 檢查協議參數一致性
   - 心跳間隔：3 分鐘 (所有文件)
   - JSONL 限制：≤10 個 (所有文件)
   - Streaming 塊大小：2000 tokens (所有文件)
   
3. 檢查 GDI 閾值一致性
   - ≥95: Promoted
   - 70-94: Active
   - 40-69: Review
   - <40: Stale
```

### 階段 2: 協議文件時效性檢查
```
1. 檢查文件創建時間
   - > 30 天未更新 → 標記為 review
   
2. 檢查引用有效性
   - API 端點是否仍存在
   - 路徑是否有效
   
3. 檢查任務狀態
   - 已完成任務 → 歸檔
   - 進行中任務 → 更新進度
   - 失敗任務 → 分析原因
```

### 階段 3: 學習記錄價值評估
```
1. 評估每個 .learnings/ 文件
   - 引用次數
   - 實用性評分
   - 時效性
   
2. 識別高價值學習
   - 可轉化為基因
   - 可蒸餾為技能
   - 可整合到 Wiki
   
3. 識別低價值學習
   - 過時信息
   - 重複內容
   - 錯誤記錄
```

---

## 審計結果預期

### 高價值發現
- 可優化資產清單
- 可蒸餾模式
- 可整合知識

### 待修復問題
- 邏輯矛盾
- 過時引用
- 配置不一致

### 待修剪資產
- GDI < 40 (預計 0 個)
- 170 天未 FETCH (預計 0 個)

---

## 自動化審計腳本

### 腳本 1: 簽名一致性檢查
```bash
#!/bin/bash
# check_signatures.sh
grep -r "RedAgent Team" /home/admin/.openclaw/workspace/*.md | \
  grep -v "🦞RedOpenClaw" && echo "⚠️ 簽名不一致" || echo "✅ 簽名一致"
```

### 腳本 2: GDI 閾值檢查
```bash
#!/bin/bash
# check_gdi_thresholds.sh
# 掃描所有 JSON 文件的 GDI 相關配置
```

### 腳本 3: 過時文件檢測
```bash
#!/bin/bash
# check_stale_files.sh
find /home/admin/.openclaw/workspace -name "*.md" -mtime +30
```

---

## 執行時間表

| 時間 | 任務 | 產出 |
|------|------|------|
| T+0min | 配置文件檢查 | 一致性報告 |
| T+10min | 協議文件檢查 | 時效性報告 |
| T+20min | 學習記錄檢查 | 價值評估報告 |
| T+30min | 生成審計報告 | p3-lint-report.md |
| T+40min | 執行修剪 (如有) | 修剪日誌 |

---

## 風險緩解

### 風險 1: 誤刪高價值資產
- **對策**: 修剪前二次確認
- **備案**: 保留備份 30 天

### 風險 2: IO 過載
- **對策**: 增量審計，每次 1 個目錄
- **備案**: 監控交換空間

### 風險 3: 審計中斷
- **對策**: 每 3 分鐘心跳
- **備案**: 斷點續審

---

**簽名**: RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...
