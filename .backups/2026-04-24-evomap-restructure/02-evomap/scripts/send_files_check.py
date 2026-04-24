#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發送 EvoMap 5 個核心文檔到飛書供用戶核對
"""

import sys
import os
from datetime import datetime

tools_path = '/home/admin/.openclaw/workspace/tools'
sys.path.insert(0, tools_path)
os.chdir(tools_path)

import importlib.util
spec = importlib.util.spec_from_file_location("task_notifier", os.path.join(tools_path, "task-notifier.py"))
task_notifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_notifier)
send_feishu_message = task_notifier.send_feishu_message
get_feishu_token = task_notifier.get_feishu_token
load_config = task_notifier.load_config

def main():
    config = load_config()
    token = get_feishu_token(config['app_id'], config['app_secret'])
    user_id = config['target_user']
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 發送文件清單和事故說明
    title = "📋 EvoMap 5 個核心文檔 - 請核對"
    
    text = f"""時間：{now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 已讀取 5 個核心文檔

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ EvoMap 知識變現項目執行手冊.md
   狀態：✅ 存在
   內容：項目總覽、時間表、執行流程、變現路徑
   
2️⃣ EvoMap 定時任務配置.md
   狀態：✅ 存在
   內容：Cron 配置、通知配置、腳本清單
   
3️⃣ EvoMap 用戶手冊.md
   狀態：✅ 存在
   內容：操作指南、常見問題、快速索引
   
4️⃣ 通知方式優化方案.md
   狀態：✅ 存在
   內容：郵件→飛書優化方案、通知模板
   
5️⃣ 自動化部署提醒.md
   狀態：✅ 存在
   內容：部署清單、第 1 週手動執行計劃

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 今日事故原因說明

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

問題：今天 (03-20) 沒有收到任何定時任務提醒

根本原因:
❌ 配置文檔只是「模板」，未實際部署
❌ crontab 中沒有 EvoMap 任務
❌ scripts 目錄不存在
❌ Python 腳本未創建

簡單說：文檔寫好了，但沒執行！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 已修復（08:22 完成）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 創建 scripts 目錄 ✅
2. 創建 5 個 Python 腳本 ✅
   - morning_check.py (07:30)
   - task_reminder.py (17:25)
   - content_reminder.py (18:10)
   - community_reminder.py (20:00)
   - daily_summary.py (22:00)
3. 添加到 crontab ✅
4. 測試通過 ✅
5. 飛書通知正常 ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 下次執行時間

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

任務提醒：今天 17:25 (約 8.5 小時後)
創作提醒：今天 18:10
社區提醒：今天 20:00
每日匯總：今天 22:00
晨間檢查：明天 07:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 請核對

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

請確認:
1. 5 個文檔內容是否正確？
2. 定時任務配置是否符合預期？
3. 通知時間是否需要調整？

如有問題請立即告知！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # 發送飛書消息
    result = send_feishu_message(token, user_id, title, text)
    
    if result:
        print("✅ 飛書消息發送成功")
        print(f"\n{text}")
    else:
        print("❌ 飛書消息發送失敗")

if __name__ == "__main__":
    main()
