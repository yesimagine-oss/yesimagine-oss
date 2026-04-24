#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书 API 实战代码示例
Feishu API Practical Examples

使用方法:
1. 复制 .env.example 为 .env
2. 填写 App ID 和 App Secret
3. 运行示例代码

作者：OpenClaw Agent
创建时间：2026-03-13
"""

import os
import json
import time
import hashlib
import base64
import hmac
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# ============================================================================
# 1. Token 管理器
# ============================================================================

class FeishuTokenManager:
    """飞书 Token 管理器 - 自动获取和刷新 Token"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_access_token: Optional[str] = None
        self.token_expire_time: float = 0
    
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
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取 Token 失败：{result.get('msg')}")
        
        self.app_access_token = result["app_access_token"]
        # Token 有效期 2 小时，提前 10 分钟刷新
        self.token_expire_time = time.time() + 7200 - 600
        
        print(f"✅ 获取新 Token 成功，有效期至 {datetime.fromtimestamp(self.token_expire_time)}")
        return self.app_access_token
    
    def refresh_token(self):
        """强制刷新 Token"""
        self.app_access_token = None
        self.token_expire_time = 0
        return self.get_app_access_token()


# ============================================================================
# 2. 飞书 API 客户端
# ============================================================================

class FeishuClient:
    """飞书 API 客户端 - 封装常用 API"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.token_manager = FeishuTokenManager(app_id, app_secret)
        self.base_url = "https://open.feishu.cn"
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.token_manager.get_app_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """发送 HTTP 请求"""
        headers = self._get_headers()
        response = requests.request(method, url, headers=headers, **kwargs)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"API 调用失败：{result.get('msg')} (code: {result.get('code')})")
        
        return result
    
    # ==================== 消息 API ====================
    
    def send_text_message(self, receive_id: str, text: str, msg_type: str = "user") -> str:
        """
        发送文本消息
        
        Args:
            receive_id: 接收者 ID (user_id/open_id/chat_id)
            text: 消息文本
            msg_type: ID 类型 (user/open/chat)
        
        Returns:
            message_id: 消息 ID
        """
        url = f"{self.base_url}/open-apis/im/v1/messages"
        params = {"receive_id_type": msg_type}
        payload = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        
        result = self._request("POST", url, params=params, json=payload)
        message_id = result["data"]["message_id"]
        print(f"✅ 消息发送成功，Message ID: {message_id}")
        return message_id
    
    def send_post_message(self, receive_id: str, content: List[List[Dict]], msg_type: str = "user") -> str:
        """
        发送富文本消息
        
        Args:
            receive_id: 接收者 ID
            content: 富文本内容 (二维数组)
            msg_type: ID 类型
        
        Returns:
            message_id: 消息 ID
        
        示例:
        content = [
            [
                {"tag": "text", "text": "你好，"},
                {"tag": "a", "text": "点击这里", "href": "https://example.com"},
                {"tag": "text", "text": "查看详情"}
            ]
        ]
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
        
        result = self._request("POST", url, params=params, json=payload)
        message_id = result["data"]["message_id"]
        print(f"✅ 富文本消息发送成功，Message ID: {message_id}")
        return message_id
    
    def send_interactive_card(self, receive_id: str, card_content: Dict, msg_type: str = "user") -> str:
        """
        发送交互式卡片消息
        
        Args:
            receive_id: 接收者 ID
            card_content: 卡片内容 (字典)
            msg_type: ID 类型
        
        Returns:
            message_id: 消息 ID
        """
        url = f"{self.base_url}/open-apis/im/v1/messages"
        params = {"receive_id_type": msg_type}
        payload = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(card_content)
        }
        
        result = self._request("POST", url, params=params, json=payload)
        message_id = result["data"]["message_id"]
        print(f"✅ 卡片消息发送成功，Message ID: {message_id}")
        return message_id
    
    # ==================== 用户 API ====================
    
    def get_user_info(self, user_id: str, id_type: str = "user_id") -> Dict[str, Any]:
        """
        获取用户信息
        
        Args:
            user_id: 用户 ID
            id_type: ID 类型 (user_id/open_id/union_id)
        
        Returns:
            用户信息字典
        """
        url = f"{self.base_url}/open-apis/contact/v3/users/{user_id}"
        params = {"user_id_type": id_type}
        
        result = self._request("GET", url, params=params)
        user = result["data"]["user"]
        
        print(f"✅ 获取用户信息成功：{user.get('name')} ({user.get('email')})")
        return user
    
    def batch_get_users(self, user_ids: List[str]) -> List[Dict[str, Any]]:
        """
        批量获取用户信息
        
        Args:
            user_ids: 用户 ID 列表
        
        Returns:
            用户信息列表
        """
        url = f"{self.base_url}/open-apis/contact/v3/users/batch"
        payload = {"user_ids": user_ids}
        
        result = self._request("POST", url, json=payload)
        users = result["data"]["items"]
        
        print(f"✅ 批量获取用户信息成功，共 {len(users)} 个用户")
        return users
    
    # ==================== 日历 API ====================
    
    def create_calendar_event(self, calendar_id: str, summary: str, start_time: int, end_time: int, 
                             attendees: Optional[List[str]] = None) -> str:
        """
        创建日历事件
        
        Args:
            calendar_id: 日历 ID
            summary: 事件标题
            start_time: 开始时间戳 (秒)
            end_time: 结束时间戳 (秒)
            attendees: 参会人用户 ID 列表
        
        Returns:
            event_id: 事件 ID
        """
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{calendar_id}/events"
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
        
        if attendees:
            payload["attendees"] = [
                {"user_id": uid, "type": "user"} for uid in attendees
            ]
        
        result = self._request("POST", url, json=payload)
        event_id = result["data"]["event_id"]
        
        print(f"✅ 日历事件创建成功，Event ID: {event_id}")
        return event_id
    
    def get_calendar_events(self, calendar_id: str, time_min: int, time_max: int, 
                           max_results: int = 10) -> List[Dict[str, Any]]:
        """
        查询日历事件
        
        Args:
            calendar_id: 日历 ID
            time_min: 开始时间戳
            time_max: 结束时间戳
            max_results: 最大返回数量
        
        Returns:
            事件列表
        """
        url = f"{self.base_url}/open-apis/calendar/v4/calendars/{calendar_id}/events"
        params = {
            "time_min": str(time_min),
            "time_max": str(time_max),
            "max_results": max_results
        }
        
        result = self._request("GET", url, params=params)
        events = result["data"]["items"]
        
        print(f"✅ 查询日历事件成功，共 {len(events)} 个事件")
        return events
    
    # ==================== 云文档 API ====================
    
    def create_document(self, folder_token: str, title: str, doc_type: str = "docx") -> str:
        """
        创建云文档
        
        Args:
            folder_token: 文件夹 Token
            title: 文档标题
            doc_type: 文档类型 (docx/sheet/file)
        
        Returns:
            file_token: 文件 Token
        """
        url = f"{self.base_url}/open-apis/drive/v1/files"
        payload = {
            "folder_token": folder_token,
            "title": title,
            "type": doc_type
        }
        
        result = self._request("POST", url, json=payload)
        file_token = result["data"]["file_token"]
        
        print(f"✅ 云文档创建成功，File Token: {file_token}")
        return file_token
    
    def get_document_info(self, file_token: str) -> Dict[str, Any]:
        """
        获取云文档信息
        
        Args:
            file_token: 文件 Token
        
        Returns:
            文档信息字典
        """
        url = f"{self.base_url}/open-apis/drive/v1/files/{file_token}"
        
        result = self._request("GET", url)
        doc_info = result["data"]
        
        print(f"✅ 获取文档信息成功：{doc_info.get('title')}")
        return doc_info


# ============================================================================
# 3. 消息卡片构建器
# ============================================================================

class CardBuilder:
    """飞书消息卡片构建器"""
    
    @staticmethod
    def build_notification_card(title: str, content: str, level: str = "info") -> Dict:
        """
        构建通知卡片
        
        Args:
            title: 标题
            content: 内容
            level: 级别 (info/warning/error/success)
        
        Returns:
            卡片内容字典
        """
        colors = {
            "info": "#3370ff",
            "warning": "#ff7a45",
            "error": "#f54848",
            "success": "#00b42a"
        }
        
        return {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": colors.get(level, "#3370ff"),
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": content
                    }
                }
            ]
        }
    
    @staticmethod
    def build_button_card(title: str, content: str, button_text: str, 
                         button_url: str) -> Dict:
        """
        构建按钮卡片
        
        Args:
            title: 标题
            content: 内容
            button_text: 按钮文本
            button_url: 按钮链接
        
        Returns:
            卡片内容字典
        """
        return {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "#3370ff",
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": content
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": button_text
                            },
                            "type": "primary",
                            "url": button_url
                        }
                    ]
                }
            ]
        }
    
    @staticmethod
    def build_markdown_card(title: str, markdown_content: str) -> Dict:
        """
        构建 Markdown 卡片
        
        Args:
            title: 标题
            markdown_content: Markdown 内容
        
        Returns:
            卡片内容字典
        """
        return {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "#3370ff",
                "title": {
                    "tag": "plain_text",
                    "content": title
                }
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": markdown_content
                }
            ]
        }


# ============================================================================
# 4. 示例代码
# ============================================================================

def example_send_message():
    """示例 1: 发送消息"""
    # 从环境变量获取配置
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    user_id = os.getenv("FEISHU_USER_ID")
    
    if not all([app_id, app_secret, user_id]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_USER_ID")
        return
    
    # 创建客户端
    client = FeishuClient(app_id, app_secret)
    
    # 发送文本消息
    client.send_text_message(user_id, "你好，这是测试消息！")
    
    # 发送富文本消息
    content = [
        [
            {"tag": "text", "text": "你好，"},
            {"tag": "a", "text": "点击这里", "href": "https://open.feishu.cn"},
            {"tag": "text", "text": "查看飞书开放平台"}
        ]
    ]
    client.send_post_message(user_id, content)
    
    # 发送卡片消息
    card = CardBuilder.build_notification_card(
        title="测试通知",
        content="这是一条测试通知消息",
        level="success"
    )
    client.send_interactive_card(user_id, card)


def example_get_user_info():
    """示例 2: 获取用户信息"""
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    user_id = os.getenv("FEISHU_USER_ID")
    
    if not all([app_id, app_secret, user_id]):
        print("❌ 请设置环境变量")
        return
    
    client = FeishuClient(app_id, app_secret)
    
    # 获取单个用户信息
    user = client.get_user_info(user_id)
    print(f"用户：{user['name']}, 邮箱：{user['email']}, 部门：{user.get('department_ids', [])}")
    
    # 批量获取用户信息
    users = client.batch_get_users([user_id])
    for u in users:
        print(f"用户：{u['name']}, 职位：{u.get('job_title', 'N/A')}")


def example_calendar():
    """示例 3: 日历管理"""
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    calendar_id = os.getenv("FEISHU_CALENDAR_ID")
    
    if not all([app_id, app_secret, calendar_id]):
        print("❌ 请设置环境变量")
        return
    
    client = FeishuClient(app_id, app_secret)
    
    # 创建日历事件
    now = int(time.time())
    event_id = client.create_calendar_event(
        calendar_id=calendar_id,
        summary="测试会议",
        start_time=now + 3600,  # 1 小时后
        end_time=now + 7200,    # 2 小时后
        attendees=[]
    )
    
    # 查询日历事件
    events = client.get_calendar_events(
        calendar_id=calendar_id,
        time_min=now,
        time_max=now + 86400 * 7,  # 7 天内
        max_results=10
    )
    
    for event in events:
        print(f"事件：{event['summary']}, 开始：{event['start_time']}")


def example_document():
    """示例 4: 云文档管理"""
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    folder_token = os.getenv("FEISHU_FOLDER_TOKEN")
    
    if not all([app_id, app_secret, folder_token]):
        print("❌ 请设置环境变量")
        return
    
    client = FeishuClient(app_id, app_secret)
    
    # 创建文档
    file_token = client.create_document(
        folder_token=folder_token,
        title=f"测试文档 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    
    # 获取文档信息
    doc_info = client.get_document_info(file_token)
    print(f"文档：{doc_info['title']}, 类型：{doc_info['type']}")


# ============================================================================
# 5. 主函数
# ============================================================================

def main():
    """主函数 - 选择运行示例"""
    print("=" * 60)
    print("飞书 API 实战示例")
    print("=" * 60)
    print()
    print("请选择要运行的示例:")
    print("1. 发送消息")
    print("2. 获取用户信息")
    print("3. 日历管理")
    print("4. 云文档管理")
    print()
    
    choice = input("请输入选项 (1-4): ").strip()
    
    if choice == "1":
        example_send_message()
    elif choice == "2":
        example_get_user_info()
    elif choice == "3":
        example_calendar()
    elif choice == "4":
        example_document()
    else:
        print("❌ 无效选项")


if __name__ == "__main__":
    main()
