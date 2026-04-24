"""
飞书通知机器人单元测试
Feishu Notification Bot Unit Tests
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# 测试 Token 管理器
class TestFeishuTokenManager(unittest.TestCase):
    """Token 管理器测试"""
    
    def setUp(self):
        """测试前准备"""
        from feishu_common import FeishuTokenManager
        self.token_manager = FeishuTokenManager("test_app_id", "test_app_secret")
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.token_manager.app_id, "test_app_id")
        self.assertEqual(self.token_manager.app_secret, "test_app_secret")
        self.assertIsNone(self.token_manager.app_access_token)
    
    @patch('feishu_common.requests.post')
    def test_get_token_success(self, mock_post):
        """测试获取 Token 成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "app_access_token": "test_token"
        }
        mock_post.return_value = mock_response
        
        token = self.token_manager.get_app_access_token()
        
        self.assertEqual(token, "test_token")
        self.assertIsNotNone(self.token_manager.token_expire_time)
    
    @patch('feishu_common.requests.post')
    def test_get_token_failure(self, mock_post):
        """测试获取 Token 失败"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 99991663,
            "msg": "invalid app_access_token"
        }
        mock_post.return_value = mock_response
        
        with self.assertRaises(Exception):
            self.token_manager.get_app_access_token()

# 测试消息模板
class TestMessageTemplates(unittest.TestCase):
    """消息模板测试"""
    
    def test_daily_report(self):
        """测试日报模板"""
        from projects.feishu_notification_bot.bot_v2 import MessageTemplates
        
        card = MessageTemplates.daily_report("工作日报", "今日工作内容")
        
        self.assertIn("header", card)
        self.assertIn("elements", card)
        self.assertEqual(card["header"]["template"], "#3370ff")
    
    def test_meeting_reminder(self):
        """测试会议提醒模板"""
        from projects.feishu_notification_bot.bot_v2 import MessageTemplates
        
        card = MessageTemplates.meeting_reminder("项目会议", "2026-03-14 14:00")
        
        self.assertIn("header", card)
        self.assertEqual(card["header"]["template"], "#ff7a45")
    
    def test_alert_message(self):
        """测试告警消息模板"""
        from projects.feishu_notification_bot.bot_v2 import MessageTemplates
        
        card = MessageTemplates.alert_message("error", "错误通知", "错误内容")
        
        self.assertEqual(card["header"]["template"], "#f54848")

# 测试数据库
class TestNotificationDB(unittest.TestCase):
    """数据库测试"""
    
    def setUp(self):
        """测试前准备"""
        from projects.feishu_notification_bot.bot_v2 import NotificationDB
        self.db = NotificationDB(":memory:")
    
    def tearDown(self):
        """测试后清理"""
        self.db.conn.close()
    
    def test_log_notification(self):
        """测试记录通知"""
        self.db.log_notification("user123", "text", "测试消息", "success")
        
        results = self.db.execute("SELECT * FROM notifications")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "user123")
    
    def test_get_stats(self):
        """测试获取统计"""
        self.db.log_notification("user123", "text", "消息 1", "success")
        self.db.log_notification("user123", "text", "消息 2", "fail")
        
        stats = self.db.get_stats()
        
        self.assertIn("success", stats)
        self.assertIn("fail", stats)
        self.assertEqual(stats["success"], 1)
        self.assertEqual(stats["fail"], 1)

if __name__ == "__main__":
    unittest.main()
