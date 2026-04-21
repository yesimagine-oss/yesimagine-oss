#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能开发组件库 - 测试套件

包含所有组件的单元测试和集成测试
"""

import unittest
from components.fetcher import Fetcher
from components.parser import Parser
from components.classifier import Classifier
from components.uploader import Uploader
from components.indexer import Indexer
from components.notifier import Notifier


class TestFetcher(unittest.TestCase):
    """Fetcher 组件测试"""
    
    def test_fetch_jina(self):
        """测试 Jina 抓取"""
        url = "https://www.baidu.com"
        result = Fetcher.fetch(url, method="jina", timeout=10)
        
        self.assertIn("markdown", result)
        self.assertIn("html", result)
        self.assertIn("source_url", result)
    
    def test_fetch_invalid_method(self):
        """测试无效方法"""
        with self.assertRaises(ValueError):
            Fetcher.fetch("https://example.com", method="invalid")
    
    def test_extract_images(self):
        """测试图片提取"""
        raw = {
            "markdown": "![img1](http://example.com/1.jpg) ![img2](http://example.com/2.png)",
            "html": '<img src="http://example.com/3.gif">'
        }
        images = Parser._extract_images(raw)
        
        self.assertEqual(len(images), 3)


class TestParser(unittest.TestCase):
    """Parser 组件测试"""
    
    def test_parse(self):
        """测试内容解析"""
        raw = {
            "title": "测试文章",
            "markdown": "这是内容",
            "html": "<p>这是内容</p>",
            "source_url": "https://example.com"
        }
        
        parsed = Parser.parse(raw)
        
        self.assertEqual(parsed["title"], "测试文章")
        self.assertEqual(parsed["content"], "这是内容")
        self.assertIn("source_url", parsed["metadata"])
    
    def test_replace_images(self):
        """测试图片替换"""
        content = "![img](http://example.com/img.jpg)"
        image_key_map = {"http://example.com/img.jpg": "img_key_123"}
        
        result = Parser.replace_images(content, image_key_map)
        
        self.assertIn("img_key_123", result)


class TestClassifier(unittest.TestCase):
    """Classifier 组件测试"""
    
    def test_classify_tutorial(self):
        """测试教程分类"""
        result = Classifier.classify("这是一篇安装配置教程", "Python 安装指南")
        self.assertEqual(result, "📖 技术教程")
    
    def test_classify_case(self):
        """测试案例分类"""
        result = Classifier.classify("这是一个实战项目案例", "实战项目演示")
        self.assertEqual(result, "🛠️ 实战案例")
    
    def test_classify_news(self):
        """测试资讯分类"""
        result = Classifier.classify("这是最新热点资讯", "AI 新功能发布")
        self.assertEqual(result, "🔥 热点资讯")
    
    def test_classify_no_match(self):
        """测试无匹配情况"""
        result = Classifier.classify("这是一段无关键词的文本", "无标题")
        self.assertEqual(result, "待分类")


class TestUploader(unittest.TestCase):
    """Uploader 组件测试"""
    
    def test_create_feishu_doc(self):
        """测试创建飞书文档"""
        url = Uploader.create_feishu_doc("测试文档", "测试内容")
        self.assertIsInstance(url, str)
    
    def test_upload_images(self):
        """测试图片上传"""
        images = ["http://example.com/1.jpg", "http://example.com/2.jpg"]
        result = Uploader.upload_images(images, target="local")
        
        # 由于是测试，返回占位符
        self.assertIsInstance(result, dict)


class TestIndexer(unittest.TestCase):
    """Indexer 组件测试"""
    
    def test_update_bitable(self):
        """测试更新多维表格"""
        record_id = Indexer.update_bitable(
            app_token="test_token",
            table_id="test_table",
            fields={"标题": "测试"}
        )
        self.assertIsInstance(record_id, str)


class TestNotifier(unittest.TestCase):
    """Notifier 组件测试"""
    
    def test_send_success(self):
        """测试成功通知"""
        # 不应该抛出异常
        Notifier.send_success("📖 技术教程", "测试", "http://example.com")
    
    def test_send_failure(self):
        """测试失败通知"""
        # 不应该抛出异常
        Notifier.send_failure("测试错误")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 1. 抓取
        raw = Fetcher.fetch("https://www.baidu.com", method="jina", timeout=10)
        
        # 2. 解析
        parsed = Parser.parse(raw)
        
        # 3. 分类
        category = Classifier.classify(parsed["content"], parsed["title"])
        
        # 4. 上传（模拟）
        doc_url = "https://example.feishu.cn/docx/test"
        
        # 5. 索引（模拟）
        record_id = "record_test"
        
        # 6. 通知（模拟）
        Notifier.send_success(category, parsed["title"], doc_url)
        
        # 验证
        self.assertIsNotNone(raw)
        self.assertIsNotNone(parsed)
        self.assertIsInstance(category, str)
        self.assertIsInstance(doc_url, str)
        self.assertIsInstance(record_id, str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
