#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Content Collector 測試用例

測試覆蓋：
1. 內容類型識別
2. 元數據提取
3. Slug 生成
4. 關鍵詞提取
5. 項目匹配
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector import ContentCollector


def test_identify_type():
    """測試內容類型識別"""
    print("\n🧪 測試：內容類型識別")
    
    collector = ContentCollector()
    
    # 微信文章
    assert collector._identify_type("https://mp.weixin.qq.com/s/xxx") == "wechat"
    print("  ✅ 微信文章識別正確")
    
    # 普通網頁
    assert collector._identify_type("https://example.com/article") == "articles"
    print("  ✅ 普通網頁識別正確")


def test_generate_slug():
    """測試 Slug 生成"""
    print("\n🧪 測試：Slug 生成")
    
    collector = ContentCollector()
    
    # 中文標題
    slug = collector._generate_slug("你好，世界！")
    assert len(slug) > 0
    print(f"  ✅ '你好，世界！' → '{slug}'")
    
    # 英文標題
    slug = collector._generate_slug("Hello World")
    assert "hello" in slug.lower()
    print(f"  ✅ 'Hello World' → '{slug}'")


def test_extract_keywords():
    """測試關鍵詞提取"""
    print("\n🧪 測試：關鍵詞提取")
    
    collector = ContentCollector()
    
    text = "人工智能技術分享，機器學習深度學習教程"
    keywords = collector._extract_keywords(text)
    
    assert len(keywords) > 0
    assert len(keywords) <= 5
    print(f"  ✅ 提取 {len(keywords)} 個關鍵詞：{keywords}")


def test_match_projects():
    """測試項目匹配"""
    print("\n🧪 測試：項目匹配")
    
    collector = ContentCollector()
    
    # 匹配公眾號項目
    projects = collector._match_projects(
        "公眾號寫作技巧",
        "內容運營排版文章",
        ["寫作", "排版"]
    )
    assert "wemp-ops" in projects
    print(f"  ✅ 公眾號內容匹配：{projects}")
    
    # 匹配小紅書項目
    projects = collector._match_projects(
        "小紅書筆記怎麼寫",
        "種草配圖短內容",
        ["筆記", "種草"]
    )
    assert "xiaohongshu-ops" in projects
    print(f"  ✅ 小紅書內容匹配：{projects}")


def run_all_tests():
    """運行所有測試"""
    print("=" * 50)
    print("🧪 Content Collector 測試套件")
    print("=" * 50)
    
    try:
        test_identify_type()
        test_generate_slug()
        test_extract_keywords()
        test_match_projects()
        
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
