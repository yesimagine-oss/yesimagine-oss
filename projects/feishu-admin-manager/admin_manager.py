#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书行政管理系统
Feishu Administration Management System

功能:
- 考勤管理
- 请假申请
- 报销管理
- 会议室预订

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import requests
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

class AdminManager:
    """行政管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/workflow/v1"
    
    def get_access_token(self) -> str:
        """获取 Access Token"""
        if self.access_token:
            return self.access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
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
    
    def get_attendance_records(self, user_ids: List[str], start_date: str, end_date: str) -> List[Dict]:
        """获取考勤记录"""
        url = f"{self.base_url}/attendances"
        payload = {"user_ids": user_ids, "start_date": start_date, "end_date": end_date}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取考勤记录失败：{result.get('msg')}")
    
    def create_leave_request(self, user_id: str, leave_type: str, start_time: str, end_time: str) -> str:
        """创建请假申请"""
        url = f"{self.base_url}/leaves"
        payload = {"user_id": user_id, "leave_type": leave_type, "start_time": start_time, "end_time": end_time}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["leave_id"]
        else:
            raise Exception(f"创建请假申请失败：{result.get('msg')}")
    
    def get_leave_types(self) -> List[Dict]:
        """获取请假类型列表"""
        url = f"{self.base_url}/leave_types"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取请假类型失败：{result.get('msg')}")
    
    def get_meeting_rooms(self) -> List[Dict]:
        """查询会议室列表"""
        url = f"{self.base_url}/rooms"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"查询会议室失败：{result.get('msg')}")
    
    def book_meeting_room(self, room_id: str, user_id: str, start_time: str, end_time: str) -> str:
        """预订会议室"""
        url = f"{self.base_url}/rooms/reservations"
        payload = {"room_id": room_id, "user_id": user_id, "start_time": start_time, "end_time": end_time}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["reservation_id"]
        else:
            raise Exception(f"预订会议室失败：{result.get('msg')}")

def main():
    """主函数"""
    print("=" * 60)
    print("飞书行政管理系统 v1.0")
    print("=" * 60)
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = AdminManager(app_id, app_secret)
    
    while True:
        print("\n1. 考勤记录  2. 请假申请  3. 请假类型  4. 会议室  5. 预订会议室  6. 退出")
        choice = input("选项：").strip()
        
        try:
            if choice == "1":
                user_ids = input("用户 ID: ").strip().split(",")
                start = input("开始日期：").strip()
                end = input("结束日期：").strip()
                records = manager.get_attendance_records(user_ids, start, end)
                print(f"共 {len(records)} 条记录")
            elif choice == "2":
                user_id = input("用户 ID: ").strip()
                leave_type = input("请假类型：").strip()
                start = input("开始时间：").strip()
                end = input("结束时间：").strip()
                leave_id = manager.create_leave_request(user_id, leave_type, start, end)
                print(f"✅ 申请创建：{leave_id}")
            elif choice == "3":
                leave_types = manager.get_leave_types()
                print(f"共 {len(leave_types)} 个类型")
            elif choice == "4":
                rooms = manager.get_meeting_rooms()
                print(f"共 {len(rooms)} 个会议室")
            elif choice == "5":
                room_id = input("会议室 ID: ").strip()
                user_id = input("用户 ID: ").strip()
                start = input("开始时间：").strip()
                end = input("结束时间：").strip()
                reservation_id = manager.book_meeting_room(room_id, user_id, start, end)
                print(f"✅ 预订成功：{reservation_id}")
            elif choice == "6":
                break
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
