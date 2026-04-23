#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發送 5 個 EvoMap 核心文檔的飛書鏈接
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
    
    title = "📚 EvoMap 5 個核心文檔 - 請查看"
    
    text = f"""時間：{now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 5 個飛書文檔已創建完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

您可以直接點擊以下鏈接查看：

1️⃣  EvoMap 知識變現項目執行手冊
https://feishu.cn/docx/JGjid8xCZoaoPjxRVZ9c4qBNnLb

2️⃣ ⏰ EvoMap 定時任務配置
https://feishu.cn/docx/Msf9dbnNCoggkBxEY8HcOZRvnCh

3️⃣ 📖 EvoMap 用戶手冊
https://feishu.cn/docx/N6QwdWq5zoufAWxjZqacbyfRnBh

4️⃣ 📱 EvoMap 通知方式優化方案
https://feishu.cn/docx/SBUGdipd5o4sd9xANtScw1ANnRc

5️⃣  EvoMap 自動化部署提醒
https://feishu.cn/docx/YqasdtVL1oBXwUxsoN8c5G99nMc

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 說明

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 所有文檔都可以在飛書中直接查看和編輯
✅ 支持手機和電腦訪問
✅ 可以搜索歷史內容
✅ 可以收藏和分享

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 文檔內容

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 執行手冊：項目總覽、時間表、執行流程、變現路徑
2. 定時任務：Cron 配置、腳本清單、管理命令
3. 用戶手冊：操作指南、常見問題、快速索引
4. 通知方案：郵件→飛書優化方案、通知模板
5. 自動化部署：部署清單、第 1 週手動執行計劃

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

請查看並核對文檔內容！
如有問題請立即告知。

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
