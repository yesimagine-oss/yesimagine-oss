#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 WeChat Fetcher 測試用例

測試覆蓋：
1. URL 驗證
2. 元數據提取
3. Slug 生成
4. 關鍵詞提取
5. 反爬蟲檢測
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector import WeChatFetcher


def test_is_wechat_url():
    """測試微信 URL 驗證"""
    print("\n🧪 測試：URL 驗證")
    
    fetcher = WeChatFetcher()
    
    # 微信文章
    assert fetcher._is_wechat_url("https://mp.weixin.qq.com/s/xxx") == True
    print("  ✅ 微信文章識別正確")
    
    # 普通網頁
    assert fetcher._is_wechat_url("https://example.com/article") == False
    print("  ✅ 普通網頁識別正確")


def test_generate_slug():
    """測試 Slug 生成"""
    print("\n🧪 測試：Slug 生成")
    
    fetcher = WeChatFetcher()
    
    # 中文標題
    slug = fetcher._generate_slug("你好，世界！")
    assert len(slug) > 0
    print(f"  ✅ '你好，世界！' → '{slug}'")
    
    # 英文標題
    slug = fetcher._generate_slug("Hello World")
    assert "hello" in slug.lower()
    print(f"  ✅ 'Hello World' → '{slug}'")
    
    # 長標題
    slug = fetcher._generate_slug("這是一個很長很長很長很長很長很長很長的標題")
    assert len(slug) <= 50
    print(f"  ✅ 長標題截斷正確（長度：{len(slug)}）")


def test_extract_keywords():
    """測試關鍵詞提取"""
    print("\n🧪 測試：關鍵詞提取")
    
    fetcher = WeChatFetcher()
    
    text = "人工智能技術分享，機器學習深度學習教程"
    keywords = fetcher._extract_keywords(text)
    
    assert len(keywords) > 0
    assert len(keywords) <= 5
    print(f"  ✅ 提取 {len(keywords)} 個關鍵詞：{keywords}")


def test_is_anti_bot_page():
    """測試反爬蟲頁面檢測"""
    print("\n🧪 測試：反爬蟲檢測")
    
    fetcher = WeChatFetcher()
    
    # 正常頁面
    assert fetcher._is_anti_bot_page("<h1>正常文章內容</h1>") == False
    print("  ✅ 正常頁面識別正確")
    
    # 反爬蟲頁面
    assert fetcher._is_anti_bot_page("访问限制，請稍後再試") == True
    print("  ✅ 反爬蟲頁面識別正確")
    
    # 驗證頁面
    assert fetcher._is_anti_bot_page("安全驗證，請完成驗證") == True
    print("  ✅ 驗證頁面識別正確")


def test_extract_metadata():
    """測試元數據提取"""
    print("\n🧪 測試：元數據提取")
    
    fetcher = WeChatFetcher()
    
    content = """# 測試文章標題

這是文章內容，有很多文字...
"""
    url = "https://mp.weixin.qq.com/s/test"
    
    metadata = fetcher._extract_metadata(content, url)
    
    assert metadata['title'] == "測試文章標題"
    print(f"  ✅ 標題提取正確：{metadata['title']}")
    
    assert 'url' in metadata
    print(f"  ✅ URL 保存正確：{metadata['url']}")
    
    assert 'keywords' in metadata
    print(f"  ✅ 關鍵詞提取：{metadata['keywords']}")
    
    assert 'date' in metadata
    print(f"  ✅ 日期保存：{metadata['date']}")


def run_all_tests():
    """運行所有測試"""
    print("=" * 50)
    print("🧪 WeChat Fetcher 測試套件")
    print("=" * 50)
    
    try:
        test_is_wechat_url()
        test_generate_slug()
        test_extract_keywords()
        test_is_anti_bot_page()
        test_extract_metadata()
        
        print("\n" + "=" * 50)
        print("✅ 所有測試通過！")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"\n❌ 測試失敗：{e}")
        return False
    except Exception as e:
        print(f"\n❌ 未知錯誤：{e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
