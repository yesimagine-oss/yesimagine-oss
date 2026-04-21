---
category: llm
created_at: '2026-04-14'
tags:
- llm
- python
- 學習自動化通知系統使用指南
title: Readme Python Learning
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
# 🐍 Python 學習自動化通知系統使用指南

**創建時間:** 2026-03-16  
**版本:** 1.0

---

## 📋 系統功能

| 功能 | 觸發條件 | 通知渠道 | 發送者 |
|------|---------|---------|--------|
| **學習開始** | 手動啟動 | 飛書 + webUI | `cli_a929676f8bf81cc7` |
| **學習結束** | 手動結束 | 飛書 + webUI | `cli_a929676f8bf81cc7` |
| **停滯警告** | 自動檢測 (>1 小時無活動) | 飛書 + webUI | `cli_a929676f8bf81cc7` |

---

## 🚀 快速開始

### 1. 開始學習

```bash
# 格式：python3 tools/python-learning-notifier.py start <day> <內容> <預計時長 (秒)>

# 示例：開始 Day 1 學習，預計 3 小時
python3 /home/admin/.openclaw/workspace/tools/python-learning-notifier.py start "1" "Python 基礎語法" 10800
```

**效果:**
- ✅ 飛書收到開始通知
- ✅ webUI 顯示開始通知
- ✅ 系統開始監控學習進度

### 2. 結束學習

```bash
# 格式：python3 tools/python-learning-notifier.py end <內容> <成就 1,成就 2,...> <備註>

# 示例：結束學習，完成 3 個成就
python3 /home/admin/.openclaw/workspace/tools/python-learning-notifier.py end "Python 基礎語法" "掌握變量類型，理解循環結構，完成 10 個練習" "明天繼續學習函數"
```

**效果:**
- ✅ 飛書收到完成報告
- ✅ webUI 顯示完成報告
- ✅ 學習記錄保存到歷史

### 3. 查看當前狀態

```bash
python3 /home/admin/.openclaw/workspace/tools/python-learning-notifier.py status
```

### 4. 手動更新活動時間

```bash
# 如果學習中但系統誤判停滯，可以手動更新活動時間
python3 /home/admin/.openclaw/workspace/tools/python-learning-notifier.py update-activity
```

---

## ⚙️ 自動化配置

### 定時任務 (Cron)

系統已配置每 10 分鐘自動檢查學習停滯：

```cron
*/10 * * * * cd /home/admin/.openclaw/workspace && python3 tools/python-learning-notifier.py check-stall
```

**停滯閾值:** 1 小時 (3600 秒)  
**檢查間隔:** 10 分鐘

### 修改配置

編輯配置文件：`~/.openclaw/workspace/.config/python-learning-state.json`

```json
{
  "config": {
    "expectedDuration": 10800,    // 預計學習時長 (秒)
    "stallThreshold": 3600,       // 停滯閾值 (秒)
    "checkInterval": 300          // 檢查間隔 (秒)
  }
}
```

---

## 📊 通知示例

### 學習開始通知

```
🐍 Python 學習任務啟動 - Day 1

學習內容：Python 基礎語法
啟動時間：2026-03-16 13:00
預計結束：2026-03-16 16:00
預計時長：3 小時

✅ 學習已開始，系統將自動監控進度並發送通知。
```

### 學習完成通知

```
🐍 Python 學習任務完成 - Day 1

學習內容：Python 基礎語法
學習時長：2 小時 45 分鐘
完成時間：2026-03-16 15:45

學習成效:
✅ 掌握變量類型
✅ 理解循環結構
✅ 完成 10 個練習

備註：明天繼續學習函數
```

### 停滯警告通知

```
⚠️ Python 學習停滯提醒 - Day 1

學習內容：Python 基礎語法
停滯時長：65 分鐘
最後活動：2026-03-16 14:00

遇到問題了嗎？需要幫助嗎？
請告訴我具體卡住的地方，我會提供解決方案建議。
```

---

## 🔧 故障排除

### 飛書消息發送失敗

**可能原因:**
1. App Secret 錯誤
2. 用戶 ID 無效
3. 網絡問題

**解決方法:**
```bash
# 測試飛書連接
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_a929676f8bf81cc7",
    "app_secret": "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
  }'
```

### 定時任務未執行

**檢查 Cron 狀態:**
```bash
# 查看 Cron 日志
tail -f /var/log/cron.log

# 手動執行檢查
python3 /home/admin/.openclaw/workspace/tools/python-learning-notifier.py check-stall
```

---

## 📁 文件位置

| 文件 | 說明 |
|------|------|
| `tools/python-learning-notifier.py` | 通知系統主程序 |
| `.config/python-learning-state.json` | 學習狀態文件 |
| `.config/feishu-notification.json` | 飛書通知配置 |
| `cron/python-learning-check.json` | Cron 任務配置 |

---

## 💡 使用建議

1. **開始學習時** - 立即執行 `start` 命令
2. **休息時** - 如果休息超過 1 小時，建議先 `end` 再重新 `start`
3. **遇到問題** - 不要等待停滯警告，立即在 webUI 中提問
4. **完成學習** - 立即執行 `end` 命令，記錄學習成果

---

**系統就緒！** 🎉

開始您的第一次自動化學習通知：
```bash
python3 /home/admin/.openclaw/workspace/tools/python-learning-notifier.py start "1" "Python 基礎語法" 10800
```

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[README]]
- [[clawbrowser-readme]]
- [[README]]
