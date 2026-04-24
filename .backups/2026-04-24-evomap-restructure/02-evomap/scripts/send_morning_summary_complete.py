#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發送 EvoMap 晨間匯總完整內容到飛書（不發送服務器路徑）
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
    
    title = "📊 EvoMap 晨間匯總完整報告"
    
    text = f"""時間：{now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 EvoMap 晨間檢查報告

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 檢查項目:
- 任務列表狀態
- 聲譽值變化
- 收入統計
- 今日任務規劃

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 今日提醒

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  17:30 Claim 第一個任務
2️⃣  18:15 開始內容創作
3️⃣  20:00 社區互動
4️⃣  22:00 查看每日匯總

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 今日時間表

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

07:30  ✅ 晨間匯總
17:25  ⏳ 任務提醒
17:30  ⏳ Claim 第一個任務
18:10  ⏳ 創作提醒
18:15  ⏳ 開始內容創作
20:00  ⏳ 社區提醒
20:00  ⏳ 開始社區互動
22:00  ⏳ 每日匯總

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 第 1 天建議

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 不要追求完美，完成最重要
2. 任務選擇從簡單的開始
3. 內容創作保持真實
4. 社區互動真誠回复

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 今日寄語

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

「萬事開頭難，但開始了就成功了一半。」

今天是 EvoMap 項目第 1 天，
所有準備工作已完成，
接下來就是執行！

加油！💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 說明

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 這是完整的晨間匯總內容
✅ 所有信息都在這條消息中
✅ 無需點擊任何鏈接
✅ 明天 07:30 會準時發送

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # 發送飛書消息
    result = send_feishu_message(token, user_id, title, text)
    
    if result:
        print("✅ 晨間匯總完整內容發送成功")
    else:
        print("❌ 晨間匯總完整內容發送失敗")

if __name__ == "__main__":
    main()
