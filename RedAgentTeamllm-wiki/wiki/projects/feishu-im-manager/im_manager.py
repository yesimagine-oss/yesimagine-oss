#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书即时通讯管理系统
Feishu Instant Messaging Management System

功能:
- 发送消息
- 查询消息列表
- 消息撤回
- 创建群组
- 管理群成员

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

class IMManager:
    """即时通讯管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/im/v1"
    
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
    
    def send_message(self, receive_id: str, content: str,
                    msg_type: str = "text", chat_type: str = "user") -> str:
        """发送消息"""
        url = f"{self.base_url}/messages"
        params = {"receive_id_type": chat_type}
        payload = {"receive_id": receive_id, "msg_type": msg_type, "content": content}
        response = requests.post(url, headers=self._get_headers(), params=params, json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["message_id"]
        else:
            raise Exception(f"发送消息失败：{result.get('msg')}")
    
    def get_message_list(self, chat_id: str, page_size: int = 20) -> List[Dict]:
        """获取消息列表"""
        url = f"{self.base_url}/messages"
        params = {"chat_id": chat_id, "page_size": page_size}
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取消息列表失败：{result.get('msg')}")
    
    def recall_message(self, message_id: str) -> bool:
        """撤回消息"""
        url = f"{self.base_url}/messages/{message_id}/recall"
        response = requests.post(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        return result.get("code") == 0
    
    def create_chat(self, name: str, owner_id: str, user_ids: Optional[List[str]] = None) -> str:
        """创建群组"""
        url = f"{self.base_url}/chats"
        payload = {"name": name, "owner_id": owner_id}
        if user_ids:
            payload["user_ids"] = user_ids
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["chat_id"]
        else:
            raise Exception(f"创建群组失败：{result.get('msg')}")
    
    def get_chat_members(self, chat_id: str, page_size: int = 100) -> List[Dict]:
        """获取群成员列表"""
        url = f"{self.base_url}/chats/{chat_id}/members"
        params = {"page_size": page_size}
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取群成员列表失败：{result.get('msg')}")

def main():
    """主函数"""
    print("=" * 60)
    print("飞书即时通讯管理系统 v1.0")
    print("=" * 60)
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = IMManager(app_id, app_secret)
    
    while True:
        print("\n1. 发送消息  2. 查询消息  3. 撤回消息  4. 创建群组  5. 获取成员  6. 退出")
        choice = input("选项：").strip()
        
        try:
            if choice == "1":
                receive_id = input("接收者 ID: ").strip()
                content = input("内容：").strip()
                msg_id = manager.send_message(receive_id, content)
                print(f"✅ 发送成功：{msg_id}")
            elif choice == "2":
                chat_id = input("群聊 ID: ").strip()
                messages = manager.get_message_list(chat_id)
                print(f"共 {len(messages)} 条消息")
            elif choice == "3":
                msg_id = input("消息 ID: ").strip()
                success = manager.recall_message(msg_id)
                print("✅ 撤回" if success else "❌ 失败")
            elif choice == "4":
                name = input("群名称：").strip()
                owner_id = input("群主 ID: ").strip()
                chat_id = manager.create_chat(name, owner_id)
                print(f"✅ 创建成功：{chat_id}")
            elif choice == "5":
                chat_id = input("群聊 ID: ").strip()
                members = manager.get_chat_members(chat_id)
                print(f"共 {len(members)} 个成员")
            elif choice == "6":
                break
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
