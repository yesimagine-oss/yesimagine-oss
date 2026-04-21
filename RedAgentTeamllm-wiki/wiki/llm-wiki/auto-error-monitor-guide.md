---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Auto Error Monitor Guide
type: article
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
# 事故和錯誤自動記錄機制

**安裝時間**: 2026-04-16 21:20 GMT+8  
**狀態**: ✅ 運行中  
**服務名稱**: auto-error-monitor.service

---

## 📋 功能說明

### 自動檢測的錯誤類型

| 類型 | 說明 | 檢測條件 |
|------|------|----------|
| **API_ABORTED** | API 請求被中斷 | `openclaw:prompt-error` + `aborted` |
| **TOOL_ERROR** | 工具執行錯誤 | `isError:true` 或 `exitCode != 0` |
| **EVOLVER_ERROR** | Evolver 固化失敗 | `[Solidify]` + `FAILED` |
| **EVOLVER_HOLLOW_COMMIT** | Evolver 空提交 | `HOLLOW COMMIT` |

### 自動執行任務

1. **掃描會話歷史** - 每 5 分鐘檢查所有會話文件
2. **提取錯誤** - 自動識別並分類錯誤
3. **生成報告** - JSON + Markdown 雙格式
4. **更新索引** - 自動更新 LEARNINGS.md
5. **歸檔保存** - 按日期存儲報告

---

## 📁 報告位置

| 文件類型 | 路徑 | 說明 |
|----------|------|------|
| **JSON 報告** | `.learnings/auto-errors/YYYY-MM-DD.json` | 完整錯誤數據 |
| **Markdown 報告** | `llm-wiki/accidents/auto-YYYY-MM-DD.md` | 可讀格式報告 |
| **索引更新** | `.learnings/LEARNINGS.md` | 事故列表索引 |

---

## 🔧 服務管理

### 查看狀態
```bash
sudo systemctl status auto-error-monitor.service
```

### 查看日誌
```bash
journalctl -u auto-error-monitor.service -f
```

### 重啟服務
```bash
sudo systemctl restart auto-error-monitor.service
```

### 停止服務
```bash
sudo systemctl stop auto-error-monitor.service
```

### 禁用服務
```bash
sudo systemctl disable auto-error-monitor.service
```

---

## 📊 首次運行結果 (2026-04-16)

| 指標 | 數值 |
|------|------|
| **會話文件數** | 64 個 |
| **檢測錯誤數** | 48 起 |
| **API_ABORTED** | 23 起 |
| **TOOL_ERROR** | 16 起 |
| **EVOLVER_ERROR** | 3 起 |
| **EVOLVER_HOLLOW_COMMIT** | 6 起 |

---

## 🎯 配置選項

編輯 `/home/admin/.openclaw/scripts/auto-error-monitor.js`:

```javascript
const CONFIG = {
  sessionsDir: '/home/admin/.openclaw/agents/main/sessions',
  workspaceDir: '/home/admin/.openclaw/workspace',
  learningsDir: '/home/admin/.openclaw/workspace/.learnings',
  accidentsDir: '/home/admin/.openclaw/workspace/llm-wiki/accidents',
  checkIntervalMs: 300000, // 5 分鐘
  maxErrorsPerRun: 100
};
```

### 可調整參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `checkIntervalMs` | 300000 | 檢查間隔（毫秒） |
| `maxErrorsPerRun` | 100 | 每次運行最多處理錯誤數 |

---

## 🚨 告警閾值（未來擴展）

| 條件 | 動作 |
|------|------|
| API_ABORTED > 10/小時 | 發送告警通知 |
| TOOL_ERROR > 20/小時 | 發送告警通知 |
| 連續 EVOLVER_ERROR | 發送告警通知 |

---

## 📈 事故統計查詢

### 查看今日錯誤
```bash
cat /home/admin/.openclaw/workspace/.learnings/auto-errors/$(date +%Y-%m-%d).json | jq '.errorsByType'
```

### 查看歷史趨勢
```bash
for f in /home/admin/.openclaw/workspace/.learnings/auto-errors/*.json; do
  echo -n "$(basename $f .json): "
  jq '.totalErrors' "$f"
done
```

---

## ✅ 驗證清單

- [x] 服務已安裝 (`/etc/systemd/system/auto-error-monitor.service`)
- [x] 服務已啟動 (`active (running)`)
- [x] 服務已啟用 (`enabled`)
- [x] 首次掃描完成 (48 起錯誤)
- [x] JSON 報告生成 (`.learnings/auto-errors/2026-04-16.json`)
- [x] Markdown 報告生成 (`llm-wiki/accidents/auto-2026-04-16.md`)
- [x] LEARNINGS.md 索引更新

---

## 📝 使用示例

### 手動執行一次掃描
```bash
node /home/admin/.openclaw/scripts/auto-error-monitor.js
```

### 查看生成的報告
```bash
cat /home/admin/.openclaw/workspace/.learnings/auto-errors/2026-04-16.json | jq
```

### 查看 Markdown 報告
```bash
head -100 /home/admin/.openclaw/workspace/llm-wiki/accidents/auto-2026-04-16.md
```

---

**文檔更新**: 2026-04-16 21:22 GMT+8  
**維護者**: Red Agent Team


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[21-user_guide_image_analysis_skill]]
- [[09-auto_gene_distill]]
