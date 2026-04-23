---
category: entity
created_at: '2026-04-14'
tags:
- entity
- auto-generated
title: Evomap 定時任務配置
type: entity
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
# EvoMap 定時任務配置文件

**配置日期**: 2026-03-19  
**執行開始**: 2026-03-20  
**通知方式**: 飛書（已優化，取消郵件）

---

## 📅 Cron 定時任務配置

### 系統級定時任務 (Crontab)

```bash
# 編輯 crontab
crontab -e

# 添加以下任務:

# 每天 07:30 - 晨間檢查
30 7 * * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/morning_check.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/morning.log 2>&1

# 每天 17:25 - 任務提醒
25 17 * * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/task_reminder.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/task.log 2>&1

# 每天 18:10 - 創作提醒
10 18 * * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/content_reminder.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/content.log 2>&1

# 每天 20:00 - 社區提醒
0 20 * * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/community_reminder.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/community.log 2>&1

# 每天 22:00 - 每日匯總
0 22 * * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/daily_summary.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/daily.log 2>&1

# 每週一 17:00 - 視頻主題通知
0 17 * * 1 python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/video_schedule.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/video.log 2>&1

# 每週日 21:00 - 週複盤
0 21 * * 0 python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/weekly_review.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/weekly.log 2>&1

# 每月 1 日 08:00 - 月度目標設定
0 8 1 * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/monthly_goals.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/monthly.log 2>&1

# 每月 15 日 20:00 - 月中檢查
0 20 15 * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/mid_month_check.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/midmonth.log 2>&1

# 每月最後一天 23:00 - 月度複盤
0 23 30,31 * * python3 /home/admin/.openclaw/workspace/EvoMap 項目/scripts/monthly_review.py >> /home/admin/.openclaw/workspace/EvoMap 項目/logs/monthly_review.log 2>&1
```

---

## 🔔 通知配置

### ⚠️ 郵件通知已取消

**優化日期**: 2026-03-19  
**原因**: 避免 Gmail 網絡問題，統一使用飛書通知

~~~python
# 原郵件配置已廢棄，僅供參考
# EMAIL_CONFIG = {...}
~~~

### ✅ 飛書通知配置

```python
# /home/admin/.openclaw/workspace/EvoMap 項目/config/feishu_config.py

FEISHU_CONFIG = {
    'app_id': 'cli_a929676f8bf81cc7',
    'app_secret': 'xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs',
    'target_user': 'ou_f4919832188bcc630f8f257497fa93a4',  # 老胡
    
    # 所有通知都通過飛書發送
    'notifications': {
        'morning_check': '07:30',
        'task_reminder': '17:25',
        'content_reminder': '18:10',
        'community_reminder': '20:00',
        'daily_summary': '22:00',
    }
}
```

---

## 📋 任務執行清單

### 每日任務清單

| 時間 | 任務 | 腳本 | 通知方式 | 備註 |
|------|------|------|---------|------|
| 07:30 | 晨間檢查 | morning_check.py | 飛書 | 昨日總結 |
| 17:25 | 任務提醒 | task_reminder.py | 飛書 | 任務 Claim |
| 18:10 | 創作提醒 | content_reminder.py | 飛書 | 內容創作 |
| 20:00 | 社區提醒 | community_reminder.py | 飛書 | 社區互動 |
| 22:00 | 每日匯總 | daily_summary.py | 飛書 | 完整日報 |

### 每週任務清單

| 時間 | 任務 | 腳本 | 通知方式 | 備註 |
|------|------|------|---------|------|
| 週一 17:00 | 視頻主題 | video_schedule.py | 飛書 | 本週視頻計劃 |
| 週日 21:00 | 週複盤 | weekly_review.py | 飛書 | 週報 |

### 每月任務清單

| 時間 | 任務 | 腳本 | 通知方式 | 備註 |
|------|------|------|---------|------|
| 1 日 08:00 | 月度目標 | monthly_goals.py | 飛書 | 目標設定 |
| 15 日 20:00 | 月中檢查 | mid_month_check.py | 飛書 | 進度檢查 |
| 月末 23:00 | 月度複盤 | monthly_review.py | 飛書 | 月報 |

---

## ⚠️ 異常處理配置

### 失敗重試機制

```python
# /home/admin/.openclaw/workspace/EvoMap 項目/config/retry_config.py

RETRY_CONFIG = {
    'max_retries': 3,
    'retry_delay': 300,  # 5 分鐘
    'timeout': 30,  # 30 秒
    
    # 失敗通知
    'failure_notification': {
        'enabled': True,
        'methods': ['feishu', 'sms'],
        'threshold': 2,  # 連續失敗 2 次後通知
    }
}
```

### 異常通知

```python
# 需要立即通知的異常情況
CRITICAL_ALERTS = [
    '任務 Claim 失敗',
    '內容發布失敗',
    '郵件發送失敗',
    '數據收集失敗',
    '聲譽下降',
    '收入異常波動',
]
```

---

## 📊 日誌配置

### 日誌路徑

```bash
# 日誌目錄
/home/admin/.openclaw/workspace/EvoMap 項目/logs/

# 日誌文件
- morning.log        # 晨間檢查日誌
- task.log           # 任務提醒日誌
- content.log        # 內容創作日誌
- community.log      # 社區互動日誌
- daily.log          # 每日匯總日誌
- weekly.log         # 週複盤日誌
- monthly.log        # 月度報告日誌
```

### 日誌輪轉

```bash
# 配置日誌輪轉 (logrotate)
cat > /etc/logrotate.d/evomap << EOF
/home/admin/.openclaw/workspace/EvoMap 項目/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 admin admin
}
EOF
```

---

## 🚀 啟動腳本

### 主啟動腳本

```bash
#!/bin/bash
# /home/admin/.openclaw/workspace/EvoMap 項目/scripts/start_all.sh

echo "啟動 EvoMap 定時任務..."

# 檢查 Python 環境
python3 --version

# 安裝依賴
pip3 install -r /home/admin/.openclaw/workspace/EvoMap 項目/requirements.txt

# 添加 crontab
crontab /home/admin/.openclaw/workspace/EvoMap 項目/config/crontab

# 重啟 cron 服務
sudo systemctl restart cron

echo "定時任務已啟動！"
echo "查看日誌：tail -f /home/admin/.openclaw/workspace/EvoMap 項目/logs/*.log"
```

### 停止腳本

```bash
#!/bin/bash
# /home/admin/.openclaw/workspace/EvoMap 項目/scripts/stop_all.sh

echo "停止 EvoMap 定時任務..."

# 清空 crontab
crontab -r

# 停止 cron 服務
sudo systemctl stop cron

echo "定時任務已停止！"
```

---

## 📱 通知模板

### ⚠️ 郵件模板已廢棄

~~~html
<!-- 原郵件模板已廢棄，僅供參考 -->
<!-- <!DOCTYPE html>... -->
~~~

### ✅ 飛書消息模板

```python
# /home/admin/.openclaw/workspace/EvoMap 項目/templates/feishu/daily_summary.py

def daily_summary_template(data):
    return f"""
【EvoMap 日報】{data['date']}

💰 今日收入：¥{data['today_income']} (本月¥{data['month_income']})
🏆 聲譽：{data['reputation']} (+{data['reputation_change']})
📝 產出：文章 {data['articles']} 篇 | 視頻 {data['videos']} 個
✅ 任務：完成 {data['tasks_completed']} 個
📊 粉絲：{data['followers']} (+{data['followers_change']})

詳情請查看飛書文檔 🔗
"""
```

---

## ✅ 檢查清單

### 部署前檢查

- [ ] Python 環境已安裝
- [ ] 所有依賴已安裝
- [ ] 飛書配置正確（app_id, app_secret, target_user）
- [ ] crontab 已添加
- [ ] 日誌目錄已創建
- [ ] 權限已設置

### 每日檢查

- [ ] 晨間匯總已發送（飛書）
- [ ] 任務提醒已發送（飛書）
- [ ] 創作提醒已發送（飛書）
- [ ] 社區提醒已發送（飛書）
- [ ] 每日匯總已發送（飛書）
- [ ] 日誌正常寫入

### 每週檢查

- [ ] 視頻主題已通知（飛書）
- [ ] 週複盤已發送（飛書）
- [ ] 下週計劃已生成（飛書）
- [ ] 日誌輪轉正常

### 每月檢查

- [ ] 月度目標已設定（飛書）
- [ ] 月中檢查已執行（飛書）
- [ ] 月度複盤已發送（飛書）
- [ ] 日誌歸檔正常

---

**配置日期**: 2026-03-19  
**執行開始**: 2026-03-20  
**版本**: v1.0

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]
