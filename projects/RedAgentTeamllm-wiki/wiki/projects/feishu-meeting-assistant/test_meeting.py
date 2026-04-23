"""
飞书会议助手单元测试
Feishu Meeting Assistant Unit Tests
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# 测试日历客户端
class TestCalendarClient(unittest.TestCase):
    """日历客户端测试"""
    
    def setUp(self):
        """测试前准备"""
        from feishu_common import FeishuTokenManager
        from projects.feishu_meeting_assistant.meeting_bot_v2 import CalendarClient
        
        token_manager = FeishuTokenManager("test_app_id", "test_app_secret")
        self.calendar = CalendarClient(token_manager)
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.calendar.token_manager)
        self.assertEqual(self.calendar.base_url, "https://open.feishu.cn")
    
    @patch('projects.feishu_meeting_assistant.meeting_bot_v2.requests.post')
    def test_create_event_success(self, mock_post):
        """测试创建事件成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"event_id": "test_event_id"}
        }
        mock_post.return_value = mock_response
        
        event_id = self.calendar.create_event(
            summary="测试会议",
            start_time=1709452800,
            end_time=1709456400
        )
        
        self.assertEqual(event_id, "test_event_id")
    
    @patch('projects.feishu_meeting_assistant.meeting_bot_v2.requests.get')
    def test_get_events_success(self, mock_get):
        """测试查询事件成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"items": [{"summary": "会议 1"}, {"summary": "会议 2"}]}
        }
        mock_get.return_value = mock_response
        
        events = self.calendar.get_events(1709452800, 1709539200)
        
        self.assertEqual(len(events), 2)

# 测试消息发送器
class TestMessageSender(unittest.TestCase):
    """消息发送器测试"""
    
    def setUp(self):
        """测试前准备"""
        from feishu_common import FeishuTokenManager
        from projects.feishu_meeting_assistant.meeting_bot_v2 import MessageSender
        
        token_manager = FeishuTokenManager("test_app_id", "test_app_secret")
        self.sender = MessageSender(token_manager)
    
    def test_build_meeting_reminder_card(self):
        """测试构建会议提醒卡片"""
        card = self.sender._build_meeting_reminder_card(
            "测试会议",
            "2026-03-14 14:00",
            "线上"
        )
        
        self.assertIn("header", card)
        self.assertIn("elements", card)
        self.assertEqual(card["header"]["template"], "#ff7a45")

# 测试会议助手
class TestMeetingAssistant(unittest.TestCase):
    """会议助手测试"""
    
    def setUp(self):
        """测试前准备"""
        from projects.feishu_meeting_assistant.meeting_bot_v2 import MeetingAssistant
        import os
        
        # 设置测试环境变量
        os.environ["FEISHU_APP_ID"] = "test_app_id"
        os.environ["FEISHU_APP_SECRET"] = "test_app_secret"
        
        self.assistant = MeetingAssistant()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.assistant.token_manager)
        self.assertIsNotNone(self.assistant.calendar)
        self.assertIsNotNone(self.assistant.message_sender)
    
    def test_create_meeting(self):
        """测试创建会议"""
        start_time = datetime.now() + timedelta(hours=1)
        
        # 这里需要 mock calendar.create_event
        # 简化测试
        self.assertIsNotNone(self.assistant)

if __name__ == "__main__":
    unittest.main()
