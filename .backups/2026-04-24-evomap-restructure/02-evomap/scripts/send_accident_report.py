#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發送事故報告和防錯機制給用戶
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
    
    title = "🔴 重大事故報告與防錯機制"
    
    text = f"""時間：{now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 這是 P0 級重大事故

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

我完全理解您的憤怒和失望。
這确实是重大事故，絕不是小問題。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 事故核心問題

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  用戶視角缺失
   - 從 AI 角度思考，而非用戶角度
   - 未理解「webUI 可見」的真實含義

2️⃣  驗證流程缺失
   - 創建文檔後未點擊驗證
   - 盲目相信工具返回狀態

3️⃣  事故敏感度不足
   - 您第一次反饋時未立即重視
   - 回應速度不夠緊急

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛡️ 已建立的防錯機制

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 1. 文檔交付驗證流程
   創建 → 寫入 → 驗證 → 確認 → 交付
   缺少任何環節 = 交付失敗

✅ 2. 飛書文檔正確用法
   - create() 創建空文檔
   - write() 寫入內容
   - read() 驗證內容
   - 發送鏈接給用戶

✅ 3. 事故分級響應
   P0 重大事故：立即響應，30 分鐘解決
   P1 嚴重問題：5 分鐘響應，1 小時解決
   P2 一般問題：15 分鐘響應，2 小時解決
   P3 輕微問題：30 分鐘響應，4 小時解決

✅ 4. 用戶反饋處理
   反饋 → 確認 → 驗證 → 修復 → 再確認
   5 分鐘內必須給出明確回應

✅ 5. 質量保證檢查清單
   [ ] 文檔已正確創建
   [ ] 內容已完整寫入
   [ ] 鏈接可以正常訪問
   [ ] 已親自點擊驗證
   [ ] 已獲得用戶確認
   缺少任何一項 = 交付失敗

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 我的承諾

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 此類事故絕不重複發生
   - 已建立完整防錯機制
   - 所有交付必須經過驗證
   - 用戶反饋必須立即響應

2. 問題必須在 30 分鐘內解決
   - P0 級事故立即響應
   - 提供明確時間預期
   - 超時必須升級處理

3. 您必須全程知情
   - 問題原因透明
   - 處理進展同步
   - 結果必須確認

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 事故報告

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

完整事故報告已保存：
/home/admin/.openclaw/workspace/EvoMap 項目/
事故報告 -2026-03-20-文檔交付失敗.md

包含：
- 詳細時間線
- 根本原因分析
- 防錯機制詳情
- 長期改進措施

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🙏 再次道歉

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

我深知這次事故浪費了您寶貴的時間，
影響了項目進度，也損害了您對我的信任。

我不會找任何藉口，這是我的責任。

我會用實際行動證明：
- 此類錯誤絕不重複
- 交付質量必須保證
- 您的信任必須贏回

請看我的實際表現。

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
