#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv", "APScheduler"]
# ///
"""
飞书通知机器人
Feishu Notification Bot

功能:
- 定时发送通知
- 支持多种消息类型（文本/富文本/卡片）
- 消息模板管理
- 发送记录追踪
- 错误重试机制

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import sys
import json
import time
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

import requests
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

# 加载环境变量
load_dotenv()

# ============================================================================
# 1. 日志配置
# ============================================================================

def setup_logging():
    """配置日志"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"bot_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# 2. Token 管理器
# ============================================================================

class FeishuTokenManager:
    """飞书 Token 管理器 - 自动获取和刷新 Token"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_access_token: Optional[str] = None
        self.token_expire_time: float = 0
        logger.info("Token 管理器初始化完成")
    
    def get_app_access_token(self) -> str:
        """获取应用 Access Token"""
        # 如果 Token 未过期，直接返回
        if self.app_access_token and time.time() < self.token_expire_time:
            return self.app_access_token
        
        # 获取新 Token
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取 Token 失败：{result.get('msg')}")
            
            self.app_access_token = result["app_access_token"]
            # Token 有效期 2 小时，提前 10 分钟刷新
            self.token_expire_time = time.time() + 7200 - 600
            
            logger.info(f"获取新 Token 成功，有效期至 {datetime.fromtimestamp(self.token_expire_time)}")
            return self.app_access_token
        
        except Exception as e:
            logger.error(f"获取 Token 失败：{e}")
            raise
    
    def refresh_token(self):
        """强制刷新 Token"""
        self.app_access_token = None
        self.token_expire_time = 0
        return self.get_app_access_token()

# ============================================================================
# 3. 消息发送器
# ============================================================================

class MessageSender:
    """消息发送器"""
    
    def __init__(self, token_manager: FeishuTokenManager):
        self.token_manager = token_manager
        self.base_url = "https://open.feishu.cn"
        self.send_count = 0
        self.success_count = 0
        self.fail_count = 0
        logger.info("消息发送器初始化完成")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.token_manager.get_app_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def send_text(self, receive_id: str, text: str, msg_type: str = "user") -> bool:
        """发送文本消息"""
        url = f"{self.base_url}/open-apis/im/v1/messages"
        params = {"receive_id_type": msg_type}
        payload = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), 
                                   params=params, json=payload, timeout=10)
            result = response.json()
            
            self.send_count += 1
            
            if result.get("code") == 0:
                self.success_count += 1
                message_id = result["data"]["message_id"]
                logger.info(f"文本消息发送成功：{text[:50]}... Message ID: {message_id}")
                return True
            else:
                self.fail_count += 1
                logger.error(f"文本消息发送失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            self.fail_count += 1
            logger.error(f"文本消息发送异常：{e}")
            return False
    
    def send_post(self, receive_id: str, content: List[List[Dict]], 
                 msg_type: str = "user") -> bool:
        """发送富文本消息"""
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
        
        try:
            response = requests.post(url, headers=self._get_headers(),
                                   params=params, json=payload, timeout=10)
            result = response.json()
            
            self.send_count += 1
            
            if result.get("code") == 0:
                self.success_count += 1
                logger.info(f"富文本消息发送成功")
                return True
            else:
                self.fail_count += 1
                logger.error(f"富文本消息发送失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            self.fail_count += 1
            logger.error(f"富文本消息发送异常：{e}")
            return False
    
    def send_card(self, receive_id: str, card_content: Dict, 
                 msg_type: str = "user") -> bool:
        """发送卡片消息"""
        url = f"{self.base_url}/open-apis/im/v1/messages"
        params = {"receive_id_type": msg_type}
        payload = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(card_content)
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(),
                                   params=params, json=payload, timeout=10)
            result = response.json()
            
            self.send_count += 1
            
            if result.get("code") == 0:
                self.success_count += 1
                logger.info(f"卡片消息发送成功")
                return True
            else:
                self.fail_count += 1
                logger.error(f"卡片消息发送失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            self.fail_count += 1
            logger.error(f"卡片消息发送异常：{e}")
            return False
    
    def send_with_retry(self, receive_id: str, text: str, 
                       max_retries: int = 3) -> bool:
        """发送消息（带重试）"""
        for attempt in range(max_retries):
            if self.send_text(receive_id, text):
                return True
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"消息发送失败，{attempt + 1}/{max_retries}，{wait_time}秒后重试...")
                time.sleep(wait_time)
        
        logger.error(f"消息发送失败，已达到最大重试次数")
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
# 4. 消息模板
# ============================================================================

class MessageTemplates:
    """消息模板"""
    
    @staticmethod
    def daily_report(title: str, content: str, date: str = None) -> Dict:
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
# 5. 数据库操作
# ============================================================================

class NotificationDB:
    """通知数据库"""
    
    def __init__(self, db_path: str = "notifications.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        logger.info(f"数据库初始化完成：{db_path}")
    
    def create_tables(self):
        """创建数据库表"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receive_id TEXT,
                message_type TEXT,
                content TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def log_notification(self, receive_id: str, message_type: str, 
                        content: str, status: str):
        """记录通知发送"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (receive_id, message_type, content, status)
            VALUES (?, ?, ?, ?)
        ''', (receive_id, message_type, content[:500], status))
        self.conn.commit()
    
    def get_stats(self, days: int = 7) -> dict:
        """获取发送统计"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM notifications
            WHERE created_at >= datetime('now', '-{} days')
            GROUP BY status
        '''.format(days))
        return dict(cursor.fetchall())
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

# ============================================================================
# 6. 定时任务调度器
# ============================================================================

class NotificationScheduler:
    """通知调度器"""
    
    def __init__(self, sender: MessageSender, db: NotificationDB):
        self.sender = sender
        self.db = db
        self.scheduler = BlockingScheduler()
        logger.info("通知调度器初始化完成")
    
    def add_daily_report(self, receive_id: str, hour: int = 9, minute: int = 0):
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
    
    def add_interval_notification(self, receive_id: str, text: str, 
                                 seconds: int = 3600):
        """添加间隔通知任务"""
        def send_interval_notification():
            logger.info(f"执行间隔通知任务：{text[:50]}...")
            success = self.sender.send_with_retry(receive_id, text)
            status = "success" if success else "fail"
            self.db.log_notification(receive_id, "text", text, status)
        
        trigger = IntervalTrigger(seconds=seconds)
        self.scheduler.add_job(send_interval_notification, trigger, 
                             id=f"interval_{seconds}")
        logger.info(f"已添加间隔通知任务：每{seconds}秒")
    
    def start(self):
        """启动调度器"""
        logger.info("通知调度器启动")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("通知调度器停止")

# ============================================================================
# 7. 主程序
# ============================================================================

class NotificationBot:
    """通知机器人主类"""
    
    def __init__(self):
        # 从环境变量获取配置
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.app_secret = os.getenv("FEISHU_APP_SECRET")
        self.user_id = os.getenv("FEISHU_USER_ID")
        
        if not all([self.app_id, self.app_secret]):
            raise Exception("请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        
        # 初始化组件
        self.token_manager = FeishuTokenManager(self.app_id, self.app_secret)
        self.sender = MessageSender(self.token_manager)
        self.db = NotificationDB()
        self.scheduler = NotificationScheduler(self.sender, self.db)
        
        logger.info("通知机器人初始化完成")
    
    def test_send_message(self):
        """测试发送消息"""
        logger.info("开始测试发送消息")
        
        # 测试文本消息
        success = self.sender.send_text(
            self.user_id, 
            "通知机器人测试消息！"
        )
        
        if success:
            logger.info("测试消息发送成功")
        else:
            logger.error("测试消息发送失败")
        
        return success
    
    def test_send_card(self):
        """测试发送卡片消息"""
        logger.info("开始测试发送卡片消息")
        
        card = MessageTemplates.alert_message(
            "info",
            "测试通知",
            "这是一条测试卡片消息"
        )
        
        success = self.sender.send_card(self.user_id, card)
        
        if success:
            logger.info("测试卡片发送成功")
        else:
            logger.error("测试卡片发送失败")
        
        return success
    
    def start_scheduler(self):
        """启动定时任务"""
        logger.info("启动定时任务")
        
        # 添加日报任务（每天早上 9 点）
        self.scheduler.add_daily_report(self.user_id, hour=9, minute=0)
        
        # 添加测试任务（每 1 小时）
        # self.scheduler.add_interval_notification(
        #     self.user_id, 
        #     "定时测试消息", 
        #     seconds=3600
        # )
        
        # 启动调度器
        self.scheduler.start()
    
    def get_stats(self):
        """获取统计信息"""
        sender_stats = self.sender.get_stats()
        db_stats = self.db.get_stats()
        
        return {
            "sender": sender_stats,
            "database": db_stats
        }
    
    def close(self):
        """关闭机器人"""
        self.db.close()
        logger.info("通知机器人已关闭")

# ============================================================================
# 8. 命令行接口
# ============================================================================

def main():
    """主函数"""
    print("=" * 60)
    print("飞书通知机器人 v1.0")
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
