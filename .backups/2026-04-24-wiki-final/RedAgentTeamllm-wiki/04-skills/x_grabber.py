#!/usr/bin/env python3
"""抓取 x.com 推文"""

import requests
import re
from html import unescape

def get_latest_tweet(username):
    """抓取最新推文（簡化版）"""
    try:
        # 使用 nitter（X 的鏡像站，無需登錄）
        url = f"https://nitter.net/{username}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
        
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if resp.status_code == 200:
            # 解析推文內容
            content = resp.text
            # 查找推文內容
            match = re.search(r'<div class="tweet-content media-body"[^>]*>(.*?)</div>', content, re.DOTALL)
            if match:
                tweet = unescape(match.group(1)).strip()
                # 移除多餘空格和換行
                tweet = ' '.join(tweet.split())[:100]
                return tweet
        return "[抓取失敗]"
    except Exception as e:
        return f"[錯誤：{str(e)[:50]}]"

# 測試
if __name__ == '__main__':
    print(get_latest_tweet('NASA'))
