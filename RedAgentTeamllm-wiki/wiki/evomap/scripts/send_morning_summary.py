#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發送完整的 EvoMap 晨間匯總報告
"""

import sys
import os
from datetime import datetime, timedelta

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
    
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    
    title = "☀️【EvoMap 晨間匯總】2026-03-20（補發）"
    
    text = f"""時間：{now.strftime('%Y-%m-%d %H:%M')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 昨日總結（第 1 天）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 項目狀態：已立項
✅ 定時任務：已配置
✅ 文檔系統：已完成
⏳ 任務執行：待開始（17:30）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 成長數據

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

聲譽：待開始
粉絲：待開始
收入：待開始

今天是項目第 1 天，一切準備就緒！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 今日計劃（2026-03-20）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 核心任務：

1️⃣  17:25 任務 Claim
   - 查看 AI 推薦的 3-5 個任務
   - 選擇 1 個並 Claim
   - 開始執行任務

2️⃣  18:15 內容創作
   - 選擇 AI 準備的選題
   - 撰寫第 1 篇文章
   - 預計產出：1000-2000 字

3️⃣  20:00 社區互動
   - 回复評論（3-5 條）
   - 主動連接關鍵人物
   - 點贊收藏（5-10 次）

4️⃣  22:00 每日匯總
   - 查看今日完成情況
   - 準備明日計劃

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ 今日時間表

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

07:30  ✅ 晨間匯總（補發）
17:25  ⏳ 任務提醒
17:30  ⏳ Claim 第一個任務
18:10  ⏳ 創作提醒
18:15  ⏳ 開始內容創作
20:00  ⏳ 社區提醒
20:00  ⏳ 開始社區互動
22:00  ⏳ 每日匯總

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 今日建議

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 第 1 天不要追求完美，完成最重要
2. 任務選擇從簡單的開始
3. 內容創作保持真實，分享您的實際經歷
4. 社區互動真誠回复，不要機械化

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 今日寄語

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

「萬事開頭難，但開始了就成功了一半。」

今天是 EvoMap 項目的第 1 天，
所有準備工作已完成，
接下來就是執行、執行、再執行！

加油！💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 說明

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

這是補發的晨間匯總。

原定 07:30 發送，但因配置問題延誤。
已修復問題，明天起會準時發送。

下次發送：明天 07:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # 發送飛書消息
    result = send_feishu_message(token, user_id, title, text)
    
    if result:
        print("✅ 晨間匯總報告發送成功")
        print(f"\n{text}")
    else:
        print("❌ 晨間匯總報告發送失敗")

if __name__ == "__main__":
    main()
