#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv", "APScheduler"]
# ///
"""
飞书会议助手
Feishu Meeting Assistant

功能:
- 会议自动创建
- 会议提醒发送
- 会议纪要生成
- 参会人员管理
- 会议记录追踪

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
from apscheduler.triggers.date import DateTrigger

# 加载环境变量
load_dotenv()

# ============================================================================
# 1. 日志配置
# ============================================================================

def setup_logging():
    """配置日志"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"meeting_{datetime.now().strftime('%Y%m%d')}.log"
    
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
    """飞书 Token 管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_access_token: Optional[str] = None
        self.token_expire_time: float = 0
        logger.info("Token 管理器初始化完成")
    
    def get_app_access_token(self) -> str:
        """获取应用 Access Token"""
        if self.app_access_token and time.time() < self.token_expire_time:
            return self.app_access_token
        
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
            self.token_expire_time = time.time() + 7200 - 600
            
            logger.info(f"获取新 Token 成功")
            return self.app_access_token
        
        except Exception as e:
            logger.error(f"获取 Token 失败：{e}")
            raise
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.get_app_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

# ============================================================================
# 3. 日历 API 客户端
# ============================================================================

class CalendarClient:
    """飞书日历 API 客户端"""
    
    def __init__(self, token_manager: FeishuTokenManager):
        self.token_manager = token_manager
        self.base_url = "https://open.feishu.cn"
        self.calendar_id = os.getenv("FEISHU_CALENDAR_ID")
        logger.info("日历客户端初始化完成")
    
    def create_event(self, summary: str, start_time: int, end_time: int,
                    attendees: Optional[List[str]] = None, 
                    description: str = "") -> Optional[str]:
        """创建日历事件"""
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
        
        try:
            response = requests.post(
                url, 
                headers=self.token_manager._get_headers(),
                json=payload,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                event_id = result["data"]["event_id"]
                logger.info(f"日历事件创建成功：{summary} Event ID: {event_id}")
                return event_id
            else:
                logger.error(f"日历事件创建失败：{result.get('msg')}")
                return None
        
        except Exception as e:
            logger.error(f"日历事件创建异常：{e}")
            return None
    
    def get_events(self, time_min: int, time_max: int, 
                  max_results: int = 50) -> List[Dict]:
        """查询日历事件"""
        if not self.calendar_id:
            logger.error("未配置 Calendar ID")
            return []
        
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{self.calendar_id}/events"
        params = {
            "time_min": str(time_min),
            "time_max": str(time_max),
            "max_results": max_results
        }
        
        try:
            response = requests.get(
                url,
                headers=self.token_manager._get_headers(),
                params=params,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                events = result["data"]["items"]
                logger.info(f"查询日历事件成功，共 {len(events)} 个")
                return events
            else:
                logger.error(f"查询日历事件失败：{result.get('msg')}")
                return []
        
        except Exception as e:
            logger.error(f"查询日历事件异常：{e}")
            return []
    
    def update_event(self, event_id: str, **kwargs) -> bool:
        """更新日历事件"""
        if not self.calendar_id:
            logger.error("未配置 Calendar ID")
            return False
        
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{self.calendar_id}/events/{event_id}"
        
        try:
            response = requests.patch(
                url,
                headers=self.token_manager._get_headers(),
                json=kwargs,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                logger.info(f"日历事件更新成功：{event_id}")
                return True
            else:
                logger.error(f"日历事件更新失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            logger.error(f"日历事件更新异常：{e}")
            return False
    
    def delete_event(self, event_id: str) -> bool:
        """删除日历事件"""
        if not self.calendar_id:
            logger.error("未配置 Calendar ID")
            return False
        
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{self.calendar_id}/events/{event_id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.token_manager._get_headers(),
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                logger.info(f"日历事件删除成功：{event_id}")
                return True
            else:
                logger.error(f"日历事件删除失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            logger.error(f"日历事件删除异常：{e}")
            return False

# ============================================================================
# 4. 消息发送器
# ============================================================================

class MessageSender:
    """消息发送器"""
    
    def __init__(self, token_manager: FeishuTokenManager):
        self.token_manager = token_manager
        self.base_url = "https://open.feishu.cn"
        logger.info("消息发送器初始化完成")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.token_manager.get_app_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
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
            response = requests.post(
                url, 
                headers=self._get_headers(),
                params=params, 
                json=payload,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                logger.info(f"卡片消息发送成功")
                return True
            else:
                logger.error(f"卡片消息发送失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            logger.error(f"卡片消息发送异常：{e}")
            return False
    
    def send_meeting_reminder(self, receive_id: str, meeting_title: str,
                             start_time: str, location: str = "线上") -> bool:
        """发送会议提醒"""
        card = {
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
        
        return self.send_card(receive_id, card)

# ============================================================================
# 5. 会议助手主类
# ============================================================================

class MeetingAssistant:
    """会议助手主类"""
    
    def __init__(self):
        # 从环境变量获取配置
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.app_secret = os.getenv("FEISHU_APP_SECRET")
        self.user_id = os.getenv("FEISHU_USER_ID")
        
        if not all([self.app_id, self.app_secret]):
            raise Exception("请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        
        # 初始化组件
        self.token_manager = FeishuTokenManager(self.app_id, self.app_secret)
        self.calendar = CalendarClient(self.token_manager)
        self.message_sender = MessageSender(self.token_manager)
        self.scheduler = BlockingScheduler()
        
        logger.info("会议助手初始化完成")
    
    def create_meeting(self, title: str, start_time: datetime, 
                      duration_minutes: int = 60,
                      attendees: Optional[List[str]] = None,
                      description: str = "",
                      send_reminder: bool = True) -> Optional[str]:
        """创建会议"""
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
    print("飞书会议助手 v1.0")
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
