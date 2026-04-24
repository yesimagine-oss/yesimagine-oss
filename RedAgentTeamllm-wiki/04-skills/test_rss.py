#!/usr/bin/env python3
"""測試 RSS 訂閱"""

import feedparser
import requests

def test_rss(username):
    """測試 RSS 訂閱"""
    try:
        # 使用 nitter RSS
        url = f"https://nitter.net/{username}/rss"
        proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
        
        # 先下載 RSS
        resp = requests.get(url, proxies=proxies, timeout=10)
        feed = feedparser.parse(resp.content)
        
        if feed.entries:
            latest = feed.entries[0]
            print(f"@{username}: {latest.title[:100]}")
            return True
        else:
            print(f"@{username}: 無內容")
            return False
    except Exception as e:
        print(f"@{username}: 錯誤 - {e}")
        return False

if __name__ == '__main__':
    test_rss('NASA')
