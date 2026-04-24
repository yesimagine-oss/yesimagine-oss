#!/usr/bin/env python3
"""
飛書郵件檢查工具
檢查飛書郵箱未讀郵件
"""

import requests
import json
import sys
from datetime import datetime

# 飛書應用配置
APP_ID = "cli_a929676f8bf81cc7"
APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"

def get_access_token():
    """獲取訪問令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    response = requests.post(url, json=payload, timeout=10)
    result = response.json()
    if result.get("code") == 0:
        return result["app_access_token"]
    else:
        raise Exception(f"獲取 Token 失敗：{result.get('msg')}")

def check_mail(token):
    """檢查郵件"""
    url = "https://open.feishu.cn/open-apis/mail/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "page_size": 20,
        "unread_only": True
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"獲取郵件失敗：{result.get('msg')}")

def main():
    print("=" * 60)
    print("📧 飛書郵件檢查")
    print("=" * 60)
    print()
    
    try:
        # 獲取 token
        print("⏳ 正在獲取訪問令牌...")
        token = get_access_token()
        print("✅ 令牌獲取成功")
        print()
        
        # 檢查郵件
        print("📥 正在檢查未讀郵件...")
        mails = check_mail(token)
        
        if not mails:
            print("✅ 沒有未讀郵件")
            return
        
        print(f"📬 發現 {len(mails)} 封未讀郵件\n")
        print("-" * 60)
        
        for i, mail in enumerate(mails[:10], 1):
            print(f"{i}. {mail.get('subject', '(無主題)')}")
            print(f"   發件人：{mail.get('from', '未知')}")
            print(f"   時間：{mail.get('create_time', '未知')}")
            print()
        
        if len(mails) > 10:
            print(f"... 還有 {len(mails) - 10} 封郵件")
            
    except Exception as e:
        print(f"❌ 錯誤：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
