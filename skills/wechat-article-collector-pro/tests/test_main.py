#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章收集器 - 测试套件
"""

import unittest
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'components'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from main import collect_article


class TestCollectArticle(unittest.TestCase):
    """收集功能测试"""
    
    def test_simple_mode(self):
        """测试简化模式"""
        # 使用百度作为测试 URL（避免微信反爬）
        url = "https://www.baidu.com"
        config = {}
        
        result = collect_article(url, config, simple=True)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("title", result)
        self.assertIn("category", result)
        self.assertEqual(result["doc_url"], "")
        self.assertEqual(result["record_id"], "")
    
    def test_invalid_url(self):
        """测试无效 URL"""
        url = "https://invalid-url-test-12345.com"
        config = {}
        
        result = collect_article(url, config, simple=True)
        
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
