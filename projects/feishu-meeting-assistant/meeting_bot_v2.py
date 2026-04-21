#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv", "APScheduler"]
# ///
"""
飞书会议助手 - 优化版
Feishu Meeting Assistant - Optimized Version

功能:
- 会议自动创建
- 会议提醒发送
- 会议纪要生成
- 参会人员管理
- 会议记录追踪

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
from apscheduler.triggers.date import DateTrigger

# 使用公共模块
from feishu_common import (
    FeishuTokenManager,
    setup_logging,
    retry,
    handle_api_errors,
    APIError,
    Config,
    DatabaseMixin,
    get_timestamp,
    timestamp_to_datetime
)

# ============================================================================
# 1. 配置
# ============================================================================

config = Config("FEISHU")

# ============================================================================
# 2. 日志配置
# ============================================================================

logger = setup_logging("meeting_assistant")

# ============================================================================
# 3. 日历客户端（优化版）
# ============================================================================

class CalendarClient:
    """飞书日历 API 客户端 - 优化版"""
    
    def __init__(self, token_manager: FeishuTokenManager):
        """
        初始化日历客户端
        
        Args:
            token_manager: Token 管理器
        """
        self.token_manager = token_manager
        self.base_url = "https://open.feishu.cn"
        self.calendar_id: Optional[str] = config.get("CALENDAR_ID")
        logger.info("日历客户端初始化完成")
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def create_event(self, summary: str, start_time: int, end_time: int,
                    attendees: Optional[List[str]] = None, 
                    description: str = "") -> Optional[str]:
        """
        创建日历事件
        
        Args:
            summary: 事件标题
            start_time: 开始时间戳
            end_time: 结束时间戳
            attendees: 参会人员列表
            description: 事件描述
            
        Returns:
            Optional[str]: 事件 ID，失败返回 None
        """
        if not self.calendar_id:
            logger.error("未配置 Calendar ID")
            return None
        
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{self.calendar_id}/events"
        
        payload = {
            "summary": summary,
            "start_time": {
                "timestamp": str(start_time),
                "time_zone": "Asia/Shanghai"
            },
            "end_time": {
                "timestamp": str(end_time),
                "time_zone": "Asia/Shanghai"
            }
        }
        
        if description:
            payload["description"] = description
        
        if attendees:
            payload["attendees"] = [
                {"user_id": uid, "type": "user"} for uid in attendees
            ]
        
        result = self._request("POST", url, json=payload)
        
        if result.get("code") == 0:
            event_id = result["data"]["event_id"]
            logger.info(f"日历事件创建成功：{summary} Event ID: {event_id}")
            return event_id
        else:
            logger.error(f"日历事件创建失败：{result.get('msg')}")
            return None
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def get_events(self, time_min: int, time_max: int, 
                  max_results: int = 50) -> List[Dict]:
        """
        查询日历事件
        
        Args:
            time_min: 开始时间戳
            time_max: 结束时间戳
            max_results: 最大返回数量
            
        Returns:
            List[Dict]: 事件列表
        """
        if not self.calendar_id:
            logger.error("未配置 Calendar ID")
            return []
        
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{self.calendar_id}/events"
        params = {
            "time_min": str(time_min),
            "time_max": str(time_max),
            "max_results": max_results
        }
        
        result = self._request("GET", url, params=params)
        
        if result.get("code") == 0:
            events = result["data"]["items"]
            logger.info(f"查询日历事件成功，共 {len(events)} 个")
            return events
        else:
            logger.error(f"查询日历事件失败：{result.get('msg')}")
            return []
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def update_event(self, event_id: str, **kwargs) -> bool:
        """
        更新日历事件
        
        Args:
            event_id: 事件 ID
            **kwargs: 更新字段
            
        Returns:
            bool: 更新是否成功
        """
        if not self.calendar_id:
            logger.error("未配置 Calendar ID")
            return False
        
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{self.calendar_id}/events/{event_id}"
        
        result = self._request("PATCH", url, json=kwargs)
        
        if result.get("code") == 0:
            logger.info(f"日历事件更新成功：{event_id}")
            return True
        else:
            logger.error(f"日历事件更新失败：{result.get('msg')}")
            return False
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def delete_event(self, event_id: str) -> bool:
        """
        删除日历事件
        
        Args:
            event_id: 事件 ID
            
        Returns:
            bool: 删除是否成功
        """
        if not self.calendar_id:
            logger.error("未配置 Calendar ID")
            return False
        
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{self.calendar_id}/events/{event_id}"
        
        result = self._request("DELETE", url)
        
        if result.get("code") == 0:
            logger.info(f"日历事件删除成功：{event_id}")
            return True
        else:
            logger.error(f"日历事件删除失败：{result.get('msg')}")
            return False
    
    def _request(self, method: str, url: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        import requests
        headers = self.token_manager._get_headers()
        response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
        return response.json()

# ============================================================================
# 4. 消息发送器（优化版）
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
        logger.info("消息发送器初始化完成")
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def send_meeting_reminder(self, receive_id: str, meeting_title: str,
                             start_time: str, location: str = "线上") -> bool:
        """
        发送会议提醒
        
        Args:
            receive_id: 接收者 ID
            meeting_title: 会议标题
            start_time: 开始时间
            location: 会议地点
            
        Returns:
            bool: 发送是否成功
        """
        card = self._build_meeting_reminder_card(meeting_title, start_time, location)
        return self.send_card(receive_id, card)
    
    def _build_meeting_reminder_card(self, meeting_title: str, start_time: str,
                                    location: str) -> Dict:
        """构建会议提醒卡片"""
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
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "准时参加"
                            },
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
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
        
        result = self._request("POST", url, params=params, json=payload)
        
        if result.get("code") == 0:
            logger.info(f"卡片消息发送成功")
            return True
        else:
            logger.error(f"卡片消息发送失败：{result.get('msg')}")
            return False
    
    def _request(self, method: str, url: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        import requests
        headers = self.token_manager._get_headers()
        response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
        return response.json()

# ============================================================================
# 5. 会议助手（优化版）
# ============================================================================

class MeetingAssistant(DatabaseMixin):
    """会议助手 - 优化版主类"""
    
    def __init__(self):
        """初始化会议助手"""
        # 从环境变量获取配置
        app_id = config.get("APP_ID", required=True)
        app_secret = config.get("APP_SECRET", required=True)
        self.user_id = config.get("USER_ID")
        
        # 初始化组件
        self.token_manager = FeishuTokenManager(app_id, app_secret)
        self.calendar = CalendarClient(self.token_manager)
        self.message_sender = MessageSender(self.token_manager)
        self.scheduler = BlockingScheduler()
        
        # 初始化数据库
        super().__init__("meetings.db")
        
        logger.info("会议助手初始化完成")
    
    def _init_db(self):
        """初始化数据库表"""
        self.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE,
                title TEXT,
                start_time INTEGER,
                end_time INTEGER,
                attendees TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def create_meeting(self, title: str, start_time: datetime, 
                      duration_minutes: int = 60,
                      attendees: Optional[List[str]] = None,
                      description: str = "",
                      send_reminder: bool = True) -> Optional[str]:
        """
        创建会议
        
        Args:
            title: 会议标题
            start_time: 开始时间
            duration_minutes: 时长（分钟）
            attendees: 参会人员列表
            description: 会议描述
            send_reminder: 是否发送提醒
            
        Returns:
            Optional[str]: 事件 ID，失败返回 None
        """
        logger.info(f"创建会议：{title}")
        
        # 计算结束时间
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        # 创建日历事件
        event_id = self.calendar.create_event(
            summary=title,
            start_time=int(start_time.timestamp()),
            end_time=int(end_time.timestamp()),
            attendees=attendees,
            description=description
        )
        
        if not event_id:
            logger.error("会议创建失败")
            return None
        
        # 记录到数据库
        self._log_meeting(event_id, title, start_time, end_time, attendees)
        
        # 发送会议提醒
        if send_reminder and attendees:
            for attendee in attendees:
                self.message_sender.send_meeting_reminder(
                    attendee,
                    title,
                    start_time.strftime("%Y-%m-%d %H:%M"),
                    "线上"
                )
        
        logger.info(f"会议创建成功：{event_id}")
        return event_id
    
    def _log_meeting(self, event_id: str, title: str, start_time: datetime,
                    end_time: datetime, attendees: Optional[List[str]]):
        """记录会议到数据库"""
        attendees_json = json.dumps(attendees) if attendees else "[]"
        self.execute('''
            INSERT INTO meetings (event_id, title, start_time, end_time, attendees)
            VALUES (?, ?, ?, ?, ?)
        ''', (event_id, title, int(start_time.timestamp()), 
              int(end_time.timestamp()), attendees_json))
    
    def schedule_meeting_reminder(self, event_id: str, title: str,
                                 attendees: List[str],
                                 remind_minutes: int = 15):
        """安排会议提醒"""
        def send_reminder():
            logger.info(f"发送会议提醒：{title}")
            for attendee in attendees:
                self.message_sender.send_meeting_reminder(
                    attendee,
                    title,
                    f"{remind_minutes}分钟后",
                    "线上"
                )
        
        # 安排提醒任务
        remind_time = datetime.now() + timedelta(minutes=remind_minutes)
        trigger = DateTrigger(run_date=remind_time)
        self.scheduler.add_job(send_reminder, trigger, id=f"reminder_{event_id}")
        logger.info(f"已安排会议提醒：{remind_time}")
    
    def get_today_meetings(self) -> List[Dict]:
        """获取今天的会议"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        events = self.calendar.get_events(
            time_min=int(today_start.timestamp()),
            time_max=int(today_end.timestamp())
        )
        
        logger.info(f"今天共有 {len(events)} 个会议")
        return events
    
    def get_week_meetings(self) -> List[Dict]:
        """获取本周的会议"""
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=7)
        
        events = self.calendar.get_events(
            time_min=int(week_start.timestamp()),
            time_max=int(week_end.timestamp())
        )
        
        logger.info(f"本周共有 {len(events)} 个会议")
        return events
    
    def list_meetings(self, events: List[Dict]):
        """列出会议"""
        print("\n" + "=" * 60)
        print("会议列表")
        print("=" * 60)
        
        if not events:
            print("暂无会议")
            return
        
        for i, event in enumerate(events, 1):
            print(f"\n{i}. {event.get('summary', '无标题')}")
            print(f"   开始：{event.get('start_time', {}).get('timestamp', 'N/A')}")
            print(f"   结束：{event.get('end_time', {}).get('timestamp', 'N/A')}")
            print(f"   描述：{event.get('description', '无')}")
        
        print("=" * 60)
    
    def create_standup_meeting(self, hour: int = 9, minute: int = 30,
                              attendees: Optional[List[str]] = None):
        """创建每日站会"""
        logger.info(f"创建每日站会：{hour}:{minute:02d}")
        
        def create_daily_standup():
            now = datetime.now()
            meeting_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # 如果时间已过，设置为明天
            if meeting_time <= now:
                meeting_time += timedelta(days=1)
            
            event_id = self.create_meeting(
                title="每日站会",
                start_time=meeting_time,
                duration_minutes=15,
                attendees=attendees,
                description="每日站会：昨天做了什么？今天计划做什么？有什么阻碍？",
                send_reminder=True
            )
            
            if event_id:
                self.schedule_meeting_reminder(event_id, "每日站会", attendees or [], 5)
        
        # 每天定时创建站会
        self.scheduler.add_job(
            create_daily_standup,
            'cron',
            hour=hour,
            minute=minute,
            id="daily_standup"
        )
        
        logger.info(f"已创建每日站会定时任务：每天 {hour}:{minute:02d}")
    
    def start_scheduler(self):
        """启动调度器"""
        logger.info("会议助手调度器启动")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("会议助手调度器停止")
    
    def close(self):
        """关闭会议助手"""
        self.scheduler.shutdown()
        logger.info("会议助手已关闭")

# ============================================================================
# 6. 命令行接口
# ============================================================================

def main():
    """主函数"""
    print("=" * 60)
    print("飞书会议助手 v2.0 (优化版)")
    print("=" * 60)
    print()
    print("请选择操作:")
    print("1. 创建会议")
    print("2. 查看今天的会议")
    print("3. 查看本周的会议")
    print("4. 创建每日站会")
    print("5. 启动调度器")
    print("6. 退出")
    print()
    
    try:
        assistant = MeetingAssistant()
        
        while True:
            choice = input("请输入选项 (1-6): ").strip()
            
            if choice == "1":
                title = input("会议标题：").strip()
                start_str = input("开始时间 (YYYY-MM-DD HH:MM): ").strip()
                duration = int(input("时长 (分钟): ").strip() or "60")
                
                try:
                    start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
                    event_id = assistant.create_meeting(
                        title=title,
                        start_time=start_time,
                        duration_minutes=duration
                    )
                    
                    if event_id:
                        print(f"✅ 会议创建成功：{event_id}")
                    else:
                        print("❌ 会议创建失败")
                except Exception as e:
                    print(f"❌ 错误：{e}")
            
            elif choice == "2":
                events = assistant.get_today_meetings()
                assistant.list_meetings(events)
            
            elif choice == "3":
                events = assistant.get_week_meetings()
                assistant.list_meetings(events)
            
            elif choice == "4":
                hour = int(input("站会时间 (小时 0-23): ").strip() or "9")
                minute = int(input("站会时间 (分钟 0-59): ").strip() or "30")
                assistant.create_standup_meeting(hour, minute)
                print("✅ 每日站会已创建")
            
            elif choice == "5":
                print("启动调度器... 按 Ctrl+C 停止")
                assistant.start_scheduler()
            
            elif choice == "6":
                assistant.close()
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
