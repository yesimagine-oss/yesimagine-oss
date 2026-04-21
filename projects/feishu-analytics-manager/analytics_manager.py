#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书数据分析管理系统
Feishu Data Analytics Management System

功能:
- 应用使用统计
- 用户活跃度分析
- API 调用统计
- 消息发送统计
- 会议统计

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import requests
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

class AnalyticsManager:
    """数据分析管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/analytics/v1"
    
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
    
    def get_app_usage_stats(self, app_id: str, start_date: str, end_date: str) -> Dict:
        """获取应用使用统计"""
        url = f"{self.base_url}/app_usage"
        payload = {"app_id": app_id, "start_date": start_date, "end_date": end_date}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取应用使用统计失败：{result.get('msg')}")
    
    def get_user_activity_stats(self, start_date: str, end_date: str) -> Dict:
        """获取用户活跃度统计"""
        url = f"{self.base_url}/user_activity"
        payload = {"start_date": start_date, "end_date": end_date}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取用户活跃度统计失败：{result.get('msg')}")
    
    def get_api_usage_stats(self, start_date: str, end_date: str) -> Dict:
        """获取 API 调用统计"""
        url = f"{self.base_url}/api_usage"
        payload = {"start_date": start_date, "end_date": end_date}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取 API 调用统计失败：{result.get('msg')}")
    
    def get_message_stats(self, start_date: str, end_date: str) -> Dict:
        """获取消息发送统计"""
        url = f"{self.base_url}/message_stats"
        payload = {"start_date": start_date, "end_date": end_date}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取消息统计失败：{result.get('msg')}")
    
    def get_meeting_stats(self, start_date: str, end_date: str) -> Dict:
        """获取会议统计"""
        url = f"{self.base_url}/meeting_stats"
        payload = {"start_date": start_date, "end_date": end_date}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取会议统计失败：{result.get('msg')}")

def main():
    """主函数"""
    print("=" * 60)
    print("飞书数据分析管理系统 v1.0")
    print("=" * 60)
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = AnalyticsManager(app_id, app_secret)
    
    while True:
        print("\n1. 应用统计  2. 用户活跃度  3. API 调用  4. 消息统计  5. 会议统计  6. 退出")
        choice = input("选项：").strip()
        
        try:
            if choice == "1":
                aid = input("应用 ID: ").strip()
                start = input("开始日期：").strip()
                end = input("结束日期：").strip()
                stats = manager.get_app_usage_stats(aid, start, end)
                print(f"活跃用户：{stats.get('active_users')}")
            elif choice == "2":
                start = input("开始日期：").strip()
                end = input("结束日期：").strip()
                stats = manager.get_user_activity_stats(start, end)
                print(f"DAU: {stats.get('dau')}, WAU: {stats.get('wau')}, MAU: {stats.get('mau')}")
            elif choice == "3":
                start = input("开始日期：").strip()
                end = input("结束日期：").strip()
                stats = manager.get_api_usage_stats(start, end)
                print(f"调用次数：{stats.get('call_count')}")
            elif choice == "4":
                start = input("开始日期：").strip()
                end = input("结束日期：").strip()
                stats = manager.get_message_stats(start, end)
                print(f"发送数：{stats.get('sent_count')}")
            elif choice == "5":
                start = input("开始日期：").strip()
                end = input("结束日期：").strip()
                stats = manager.get_meeting_stats(start, end)
                print(f"会议数：{stats.get('meeting_count')}")
            elif choice == "6":
                break
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
