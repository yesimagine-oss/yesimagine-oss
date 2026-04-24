#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书会议管理系统
Feishu Meeting Management System

功能:
- 创建即时会议
- 创建预约会议
- 查询会议详情
- 管理参会人
- 获取会议录制

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import json
import requests
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

class MeetingManager:
    """会议管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis"
    
    def get_access_token(self) -> str:
        """获取 Access Token"""
        if self.access_token:
            return self.access_token
        
        url = f"{self.base_url}/auth/v3/app_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            self.access_token = result["app_access_token"]
            return self.access_token
        else:
            raise Exception(f"获取 Token 失败：{result.get('msg')}")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.get_access_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    def create_instant_meeting(self, title: str = "即时会议", duration: int = 60) -> Dict:
        """创建即时会议"""
        url = f"{self.base_url}/mina/v1/meetings"
        payload = {"title": title, "duration": duration}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"创建即时会议失败：{result.get('msg')}")
    
    def create_scheduled_meeting(self, title: str, start_time: str, end_time: str,
                                attendees: Optional[List[str]] = None) -> str:
        """创建预约会议"""
        url = f"{self.base_url}/baike/v1/meetings"
        payload = {"title": title, "start_time": start_time, "end_time": end_time}
        if attendees:
            payload["attendees"] = attendees
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["meeting_id"]
        else:
            raise Exception(f"创建预约会议失败：{result.get('msg')}")
    
    def get_meeting(self, meeting_id: str) -> Dict:
        """获取会议详情"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取会议失败：{result.get('msg')}")
    
    def get_participants(self, meeting_id: str) -> List[Dict]:
        """获取参会人列表"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}/attendees"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取参会人失败：{result.get('msg')}")
    
    def get_recordings(self, meeting_id: str) -> List[Dict]:
        """获取会议录制"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}/recordings"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取会议录制失败：{result.get('msg')}")

def main():
    """主函数"""
    print("=" * 60)
    print("飞书会议管理系统 v1.0")
    print("=" * 60)
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = MeetingManager(app_id, app_secret)
    
    while True:
        print("\n1. 创建即时会议  2. 创建预约会议  3. 查询会议  4. 获取参会人  5. 获取录制  6. 退出")
        choice = input("选项：").strip()
        
        try:
            if choice == "1":
                title = input("标题：").strip() or "即时会议"
                duration = int(input("时长 (分钟): ").strip() or "60")
                meeting = manager.create_instant_meeting(title, duration)
                print(f"✅ 会议号：{meeting.get('meeting_no')}")
            elif choice == "2":
                title = input("标题：").strip()
                start = input("开始时间：").strip()
                end = input("结束时间：").strip()
                meeting_id = manager.create_scheduled_meeting(title, start, end)
                print(f"✅ 会议 ID: {meeting_id}")
            elif choice == "3":
                meeting_id = input("会议 ID: ").strip()
                meeting = manager.get_meeting(meeting_id)
                print(f"标题：{meeting.get('title')}")
            elif choice == "4":
                meeting_id = input("会议 ID: ").strip()
                participants = manager.get_participants(meeting_id)
                print(f"共 {len(participants)} 个参会人")
            elif choice == "5":
                meeting_id = input("会议 ID: ").strip()
                recordings = manager.get_recordings(meeting_id)
                print(f"共 {len(recordings)} 个录制")
            elif choice == "6":
                break
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
