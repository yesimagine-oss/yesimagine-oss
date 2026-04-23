---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 會話管理系統使用指南
- guide
- openclaw
title: Session Management Guide
type: general
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 會話管理系統使用指南

**創建時間**: 2026-03-24  
**版本**: 1.0  
**狀態**: ✅ 已部署並運行

---

## 📋 系統概述

這是一套完整的 OpenClaw 會話管理系統，提供：

- ✅ **自動清理** - 定時清理舊會話
- ✅ **智能監控** - 超過閾值自動告警
- ✅ **詳細報告** - 每週生成分析報告
- ✅ **一鍵清理** - 手動觸發清理
- ✅ **配置靈活** - 可自定義保留策略

---

## 🚀 快速開始

### 查看當前狀態

```bash
python3 /home/admin/.openclaw/workspace/tools/session-manager.py status
```

**輸出示例**:
```
📊 會話管理狀態

會話目錄：/home/admin/.openclaw/agents/main/sessions
存在狀態：✅ 存在

當前狀態:
  會話數量：9 個
  總體積：22.47 MB
  健康狀態：✅ 健康

配置限制:
  保留天數：7 天
  最大數量：50 個
  最大體積：100 MB
  告警閾值：80 MB
```

---

## 📖 命令說明

### 1️⃣ status - 查看狀態

```bash
python3 tools/session-manager.py status
```

**功能**:
- 顯示會話數量和體積
- 列出最大的 5 個會話
- 顯示健康狀態

---

### 2️⃣ cleanup - 執行清理

```bash
# 預覽清理效果（不實際刪除）
python3 tools/session-manager.py cleanup --dry-run

# 實際執行清理
python3 tools/session-manager.py cleanup
```

**清理內容**:
- 刪除 `.deleted` 結尾的文件
- 刪除超過 7 天的舊會話
- 刪除超額會話（超過 50 個）
- 運行 OpenClaw 官方 cleanup

---

### 3️⃣ report - 生成詳細報告

```bash
python3 tools/session-manager.py report
```

**報告內容**:
- 基本統計（數量、體積、平均大小）
- 年齡分佈（<1 天、1-3 天、3-7 天等）
- 體積分佈（<100KB、100KB-1MB 等）
- 增長預測
- 優化建議

---

### 4️⃣ monitor - 監控並告警

```bash
python3 tools/session-manager.py monitor
```

**監控項目**:
- 體積超過限制（>100MB）
- 體積接近限制（>80MB）
- 數量超過限制（>50 個）
- 超期會話（>14 天）

**輸出**:
- ✅ 正常：顯示綠色通過信息
- ⚠️ 告警：顯示紅色警告信息

---

### 5️⃣ init - 初始化配置

```bash
python3 tools/session-manager.py init
```

**功能**:
- 創建配置文件
- 設置默認參數
- 可自定義配置

---

## ⚙️ 配置文件

**位置**: `/home/admin/.openclaw/workspace/tools/session-manager-config.json`

**默認配置**:
```json
{
  "retention_days": 7,          // 保留天數
  "max_count": 50,              // 最大會話數
  "max_bytes_mb": 100,          // 最大體積 (MB)
  "auto_cleanup": true,         // 是否自動清理
  "notify_on_cleanup": true,    // 清理後通知
  "alert_threshold_mb": 80      // 告警閾值 (MB)
}
```

**修改配置**:
```bash
# 編輯配置文件
nano /home/admin/.openclaw/workspace/tools/session-manager-config.json

# 重新初始化
python3 tools/session-manager.py init
```

---

## 🕐 定時任務

已自動設置以下定時任務（crontab）：

| 任務 | 時間 | 頻率 | 說明 |
|------|------|------|------|
| **清理** | 每天 03:00 | 每日 | 自動清理舊會話 |
| **監控** | 每天 08:00 | 每日 | 檢查並告警 |
| **報告** | 週日 23:30 | 每週 | 生成詳細報告 |

**查看定時任務**:
```bash
crontab -l | grep session
```

**日誌位置**:
- 清理日誌：`/tmp/session-cleanup.log`
- 監控日誌：`/tmp/session-monitor.log`
- 報告日誌：`/tmp/session-report.log`

---

## 🎯 使用場景

### 場景 1：WebUI 變卡

```bash
# 1. 查看狀態
python3 tools/session-manager.py status

# 2. 執行清理
python3 tools/session-manager.py cleanup

# 3. 驗證效果
python3 tools/session-manager.py status
```

---

### 場景 2：定期检查

```bash
# 每天早上自動監控（crontab）
# 查看監控結果
cat /tmp/session-monitor.log
```

---

### 場景 3：手動檢查

```bash
# 隨時查看狀態
python3 tools/session-manager.py status

# 預覽清理效果
python3 tools/session-manager.py cleanup --dry-run
```

---

### 場景 4：調整策略

```bash
# 1. 編輯配置文件
nano tools/session-manager-config.json

# 2. 修改參數（如保留天數改為 14 天）
{
  "retention_days": 14,
  ...
}

# 3. 測試新配置
python3 tools/session-manager.py cleanup --dry-run
```

---

## 📊 OpenClaw 原生配置

**位置**: `/home/admin/.openclaw/config.yaml`

**會話維護配置**:
```yaml
session:
  maintenance:
    mode: enforce          # warn | enforce
    maxAge: 7d             # 保留 7 天
    maxCount: 50           # 最多 50 個會話
    maxBytes: 100MB        # 總體積限制
```

**OpenClaw 原生命令**:
```bash
# 查看會話列表
openclaw sessions

# 預覽清理
openclaw sessions cleanup --dry-run

# 執行清理
openclaw sessions cleanup --enforce

# 保護特定會話
openclaw sessions cleanup --active-key "agent:main:main" --enforce
```

---

## 🔧 故障排除

### 問題 1：清理後體積沒變化

**原因**: 可能沒有超過保留期的會話

**解決**:
```bash
# 查看年齡分佈
python3 tools/session-manager.py report

# 手動刪除特定會話
rm ~/.openclaw/agents/main/sessions/[會話 ID].jsonl
```

---

### 問題 2：監控告警

**原因**: 體積或數量超過閾值

**解決**:
```bash
# 查看告警詳情
cat /tmp/session-monitor.log

# 執行清理
python3 tools/session-manager.py cleanup

# 調整閾值（如需要）
nano tools/session-manager-config.json
```

---

### 問題 3：定時任務不執行

**檢查**:
```bash
# 查看 crontab
crontab -l

# 查看日誌
cat /tmp/session-cleanup.log

# 測試執行
python3 tools/session-manager.py cleanup
```

**重啟 cron**:
```bash
sudo systemctl restart cron
```

---

## 📈 最佳實踐

### 1️⃣ 定期檢查

- 每週查看一次報告
- 每月檢查增長趨勢
- 根據實際使用調整配置

### 2️⃣ 保留策略

| 使用場景 | 保留天數 | 最大體積 |
|---------|---------|---------|
| **高頻對話** | 7 天 | 100MB |
| **中頻對話** | 14 天 | 200MB |
| **低頻對話** | 30 天 | 500MB |

### 3️⃣ 備份重要會話

```bash
# 備份當前會話
cp -r ~/.openclaw/agents/main/sessions/ ~/backup/sessions-$(date +%Y%m%d)/
```

### 4️⃣ 監控增長

```bash
# 記錄每日體積
echo "$(date +%Y-%m-%d): $(du -sm ~/.openclaw/agents/main/sessions/ | cut -f1)MB" >> ~/session-growth.log
```

---

## 🎓 技術細節

### 清理邏輯

1. **刪除 .deleted 文件** - 已標記為刪除的會話
2. **刪除超期會話** - 超過 `retention_days` 天
3. **刪除超額會話** - 超過 `max_count` 個
4. **運行官方 cleanup** - OpenClaw 內建清理

### 監控邏輯

1. **體積檢查** - 超過 `max_bytes_mb` 告警
2. **數量檢查** - 超過 `max_count` 告警
3. **超期檢查** - 超過 `retention_days * 2` 告警

### 報告邏輯

1. **統計分析** - 數量、體積、平均分佈
2. **年齡分佈** - 按天數分段統計
3. **體積分佈** - 按大小分段統計
4. **增長預測** - 線性外推預估

---

## 📚 相關文檔

- OpenClaw 官方文檔：https://docs.openclaw.ai/cli/sessions
- 會話配置參考：https://docs.openclaw.ai/gateway/configuration-reference#session
- 學習報告：`/home/admin/.openclaw/workspace/.learnings/session-management-study.md`

---

## 🆘 快速命令參考

```bash
# 查看狀態
python3 tools/session-manager.py status

# 預覽清理
python3 tools/session-manager.py cleanup --dry-run

# 執行清理
python3 tools/session-manager.py cleanup

# 生成報告
python3 tools/session-manager.py report

# 監控告警
python3 tools/session-manager.py monitor

# 查看日誌
tail -f /tmp/session-cleanup.log
tail -f /tmp/session-monitor.log

# 查看 crontab
crontab -l | grep session
```

---

**維護者**: RedOpenClaw  
**最後更新**: 2026-03-24 17:36  
**狀態**: ✅ 運行正常

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[21-user_guide_image_analysis_skill]]
- [[session-manager-ai-guide]]
