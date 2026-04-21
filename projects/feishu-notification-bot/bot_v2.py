#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv", "APScheduler"]
# ///
"""
飞书通知机器人 - 优化版
Feishu Notification Bot - Optimized Version

功能:
- 定时发送通知
- 支持多种消息类型
- 消息模板管理
- 发送记录追踪
- 错误重试机制

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v2.0 (优化版)
"""

import os
import sys
import json
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

# 使用公共模块
from feishu_common import (
    FeishuTokenManager,
    setup_logging,
    retry,
    handle_api_errors,
    APIError,
    Config,
    DatabaseMixin,
    get_timestamp
)

# ============================================================================
# 1. 配置
# ============================================================================

config = Config("FEISHU")

# ============================================================================
# 2. 日志配置
# ============================================================================

logger = setup_logging("notification_bot")

# ============================================================================
# 3. 消息发送器（优化版）
# ============================================================================

class MessageSender:
    """消息发送器 - 优化版"""
    
    def __init__(self, token_manager: FeishuTokenManager):
        """
        初始化消息发送器
        
        Args:
            token_manager: Token 管理器
        """
        self.token_manager = token_manager
        self.base_url = "https://open.feishu.cn"
        self.send_count = 0
        self.success_count = 0
        self.fail_count = 0
        logger.info("消息发送器初始化完成")
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def send_text(self, receive_id: str, text: str, msg_type: str = "user") -> bool:
        """
        发送文本消息
        
        Args:
            receive_id: 接收者 ID
            text: 消息文本
            msg_type: ID 类型
            
        Returns:
            bool: 发送是否成功
        """
        url = f"{self.base_url}/open-apis/im/v1/messages"
        params = {"receive_id_type": msg_type}
        payload = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        
        response = self._request("POST", url, params=params, json=payload)
        return self._process_response(response, "文本消息")
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def send_post(self, receive_id: str, content: List[List[Dict]], 
                 msg_type: str = "user") -> bool:
        """
        发送富文本消息
        
        Args:
            receive_id: 接收者 ID
            content: 富文本内容
            msg_type: ID 类型
            
        Returns:
            bool: 发送是否成功
        """
        url = f"{self.base_url}/open-apis/im/v1/messages"
        params = {"receive_id_type": msg_type}
        payload = {
            "receive_id": receive_id,
            "msg_type": "post",
            "content": json.dumps({
                "zh_cn": {
                    "title": "消息标题",
                    "content": content
                }
            })
        }
        
        response = self._request("POST", url, params=params, json=payload)
        return self._process_response(response, "富文本消息")
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def send_card(self, receive_id: str, card_content: Dict, 
                 msg_type: str = "user") -> bool:
        """
        发送卡片消息
        
        Args:
            receive_id: 接收者 ID
            card_content: 卡片内容
            msg_type: ID 类型
            
        Returns:
            bool: 发送是否成功
        """
        url = f"{self.base_url}/open-apis/im/v1/messages"
        params = {"receive_id_type": msg_type}
        payload = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(card_content)
        }
        
        response = self._request("POST", url, params=params, json=payload)
        return self._process_response(response, "卡片消息")
    
    def _request(self, method: str, url: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        import requests
        headers = self.token_manager._get_headers()
        response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
        return response.json()
    
    def _process_response(self, result: Dict, message_type: str) -> bool:
        """处理响应"""
        self.send_count += 1
        
        if result.get("code") == 0:
            self.success_count += 1
            logger.info(f"{message_type}发送成功")
            return True
        else:
            self.fail_count += 1
            logger.error(f"{message_type}发送失败：{result.get('msg')}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取发送统计"""
        return {
            "send_count": self.send_count,
            "success_count": self.success_count,
            "fail_count": self.fail_count,
            "success_rate": f"{self.success_count / self.send_count * 100:.2f}%" if self.send_count > 0 else "N/A"
        }

# ============================================================================
# 4. 消息模板（优化版）
# ============================================================================

class MessageTemplates:
    """消息模板 - 优化版"""
    
    @staticmethod
    def daily_report(title: str, content: str, date: Optional[str] = None) -> Dict:
        """日报模板"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "#3370ff",
                "title": {"tag": "plain_text", "content": f"📊 {title} - {date}"}
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": content}
                }
            ]
        }
    
    @staticmethod
    def meeting_reminder(meeting_title: str, start_time: str, 
                        location: str = "线上") -> Dict:
        """会议提醒模板"""
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "#ff7a45",
                "title": {"tag": "plain_text", "content": "⏰ 会议提醒"}
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**会议主题**: {meeting_title}\n**开始时间**: {start_time}\n**会议地点**: {location}"
                    }
                }
            ]
        }
    
    @staticmethod
    def alert_message(alert_level: str, title: str, content: str) -> Dict:
        """告警消息模板"""
        colors = {
            "info": "#3370ff",
            "warning": "#ff7a45",
            "error": "#f54848",
            "success": "#00b42a"
        }
        
        icons = {
            "info": "📢",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }
        
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": colors.get(alert_level, "#3370ff"),
                "title": {
                    "tag": "plain_text",
                    "content": f"{icons.get(alert_level, '📢')} {title}"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": content}
                }
            ]
        }

# ============================================================================
# 5. 数据库（优化版）
# ============================================================================

class NotificationDB(DatabaseMixin):
    """通知数据库 - 优化版"""
    
    def __init__(self, db_path: str = "notifications.db"):
        """
        初始化数据库
        
        Args:
            db_path: 数据库文件路径
        """
        super().__init__(db_path)
        logger.info(f"数据库初始化完成：{db_path}")
    
    def _init_db(self):
        """初始化数据库表"""
        self.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receive_id TEXT,
                message_type TEXT,
                content TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def log_notification(self, receive_id: str, message_type: str, 
                        content: str, status: str):
        """记录通知发送"""
        self.execute('''
            INSERT INTO notifications (receive_id, message_type, content, status)
            VALUES (?, ?, ?, ?)
        ''', (receive_id, message_type, content[:500], status))
    
    def get_stats(self, days: int = 7) -> Dict[str, int]:
        """获取发送统计"""
        results = self.execute('''
            SELECT status, COUNT(*) as count
            FROM notifications
            WHERE created_at >= datetime('now', '-{} days')
            GROUP BY status
        '''.format(days))
        return dict(results)

# ============================================================================
# 6. 通知机器人（优化版）
# ============================================================================

class NotificationBot:
    """通知机器人 - 优化版主类"""
    
    def __init__(self):
        """初始化通知机器人"""
        # 从环境变量获取配置
        app_id = config.get("APP_ID", required=True)
        app_secret = config.get("APP_SECRET", required=True)
        self.user_id = config.get("USER_ID")
        
        # 初始化组件
        self.token_manager = FeishuTokenManager(app_id, app_secret)
        self.sender = MessageSender(self.token_manager)
        self.db = NotificationDB()
        self.scheduler = BlockingScheduler()
        
        logger.info("通知机器人初始化完成")
    
    def test_send_message(self) -> bool:
        """测试发送消息"""
        logger.info("开始测试发送消息")
        
        if not self.user_id:
            logger.error("未配置用户 ID")
            return False
        
        success = self.sender.send_text(
            self.user_id, 
            "通知机器人测试消息！"
        )
        
        if success:
            logger.info("测试消息发送成功")
            self.db.log_notification(self.user_id, "text", "测试消息", "success")
        else:
            logger.error("测试消息发送失败")
            self.db.log_notification(self.user_id, "text", "测试消息", "fail")
        
        return success
    
    def test_send_card(self) -> bool:
        """测试发送卡片消息"""
        logger.info("开始测试发送卡片消息")
        
        if not self.user_id:
            logger.error("未配置用户 ID")
            return False
        
        card = MessageTemplates.alert_message(
            "info",
            "测试通知",
            "这是一条测试卡片消息"
        )
        
        success = self.sender.send_card(self.user_id, card)
        
        if success:
            logger.info("测试卡片发送成功")
            self.db.log_notification(self.user_id, "card", "测试卡片", "success")
        else:
            logger.error("测试卡片发送失败")
            self.db.log_notification(self.user_id, "card", "测试卡片", "fail")
        
        return success
    
    def start_scheduler(self):
        """启动定时任务"""
        logger.info("启动定时任务")
        
        # 添加日报任务（每天早上 9 点）
        if self.user_id:
            self._add_daily_report(self.user_id, hour=9, minute=0)
        
        # 启动调度器
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("通知调度器停止")
    
    def _add_daily_report(self, receive_id: str, hour: int = 9, minute: int = 0):
        """添加日报定时任务"""
        def send_daily_report():
            logger.info("执行日报定时任务")
            content = """
**今日工作**:
- 完成飞书 API 学习
- 开发通知机器人

**明日计划**:
- 继续优化机器人功能
- 学习日历 API
            """
            card = MessageTemplates.daily_report("工作日报", content)
            success = self.sender.send_card(receive_id, card)
            status = "success" if success else "fail"
            self.db.log_notification(receive_id, "card", content, status)
        
        trigger = CronTrigger(hour=hour, minute=minute)
        self.scheduler.add_job(send_daily_report, trigger, id="daily_report")
        logger.info(f"已添加日报定时任务：每天 {hour}:{minute:02d}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "sender": self.sender.get_stats(),
            "database": self.db.get_stats()
        }
    
    def close(self):
        """关闭机器人"""
        self.scheduler.shutdown()
        logger.info("通知机器人已关闭")

# ============================================================================
# 7. 命令行接口
# ============================================================================

def main():
    """主函数"""
    print("=" * 60)
    print("飞书通知机器人 v2.0 (优化版)")
    print("=" * 60)
    print()
    print("请选择操作:")
    print("1. 测试发送文本消息")
    print("2. 测试发送卡片消息")
    print("3. 启动定时任务")
    print("4. 查看统计信息")
    print("5. 退出")
    print()
    
    try:
        bot = NotificationBot()
        
        while True:
            choice = input("请输入选项 (1-5): ").strip()
            
            if choice == "1":
                bot.test_send_message()
            elif choice == "2":
                bot.test_send_card()
            elif choice == "3":
                print("启动定时任务... 按 Ctrl+C 停止")
                bot.start_scheduler()
            elif choice == "4":
                stats = bot.get_stats()
                print("\n发送统计:")
                print(f"  发送总数：{stats['sender']['send_count']}")
                print(f"  成功数：{stats['sender']['success_count']}")
                print(f"  失败数：{stats['sender']['fail_count']}")
                print(f"  成功率：{stats['sender']['success_rate']}")
                print("\n数据库统计:")
                for status, count in stats['database'].items():
                    print(f"  {status}: {count}")
            elif choice == "5":
                bot.close()
                print("再见！")
                break
            else:
                print("无效选项，请重新输入")
    
    except Exception as e:
        logger.error(f"程序异常：{e}")
        print(f"错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
