---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 即时通讯
- api
- 完整指南
- guide
title: Feishu Im Api Guide
type: general
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 💬 即时通讯 API 完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L3-L4

---

## 📋 即时通讯 API 概述

### 什么是即时通讯 API

```
飞书即时通讯 API 提供了完整的消息沟通能力，包括：
- 发送消息（单聊/群聊）
- 查询消息列表
- 消息撤回
- 消息回复
- 创建群组
- 管理群成员
- 消息已读未读
```

### 核心概念

```
单聊 (Direct Chat):
- 两人之间的私密对话
- 使用 user_id 作为聊天 ID

群聊 (Group Chat):
- 多人参与的群组对话
- 使用 chat_id 作为聊天 ID

消息类型:
- text: 文本消息
- post: 富文本消息
- interactive: 交互式卡片
- image: 图片消息
- file: 文件消息
- audio: 语音消息
- media: 视频消息

消息已读未读:
- 追踪消息阅读状态
- 支持批量查询
```

### API 权限

```
需要的权限:
✅ im:message (消息管理)
✅ im:chat (群组管理)
✅ im:member (成员管理)
```

---

## 🛠️ 核心 API 详解

### 1. 发送消息

```python
import requests
from typing import Dict, Any, Optional, List

def send_message(access_token: str,
                receive_id: str,
                content: str,
                msg_type: str = "text",
                chat_type: str = "user",
                uuid: Optional[str] = None) -> str:
    """
    发送消息
    
    Args:
        access_token: Access Token
        receive_id: 接收者 ID (user_id 或 chat_id)
        content: 消息内容
        msg_type: 消息类型 (text/post/interactive/image/file)
        chat_type: 聊天类型 (user/group)
        uuid: 消息 UUID（用于去重，可选）
    
    Returns:
        str: 消息 ID
    
    Example:
        # 发送文本消息
        >>> msg_id = send_message(token, "user_id", "Hello", "text", "user")
        
        # 发送富文本消息
        >>> content = json.dumps({
        ...     "zh_cn": {
        ...         "title": "标题",
        ...         "content": [[{"tag": "text", "text": "内容"}]]
        ...     }
        ... })
        >>> msg_id = send_message(token, "chat_id", content, "post", "group")
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type": chat_type}
    
    payload = {
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": content
    }
    
    if uuid:
        payload["uuid"] = uuid
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, params=params, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["message_id"]
    else:
        raise Exception(f"发送消息失败：{result.get('msg')}")
```

### 2. 查询消息列表

```python
def get_message_list(access_token: str,
                    chat_id: str,
                    page_size: int = 20,
                    direction: str = "ASC",
                    start_time: Optional[str] = None,
                    end_time: Optional[str] = None) -> list:
    """
    查询消息列表
    
    Args:
        access_token: Access Token
        chat_id: 群聊 ID
        page_size: 每页数量
        direction: 排序方向 (ASC/DESC)
        start_time: 开始时间（可选）
        end_time: 结束时间（可选）
    
    Returns:
        list: 消息列表
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {
        "chat_id": chat_id,
        "page_size": page_size,
        "direction": direction
    }
    
    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"查询消息列表失败：{result.get('msg')}")
```

### 3. 获取消息详情

```python
def get_message_detail(access_token: str, message_id: str) -> Dict:
    """
    获取消息详情
    
    Args:
        access_token: Access Token
        message_id: 消息 ID
    
    Returns:
        dict: 消息详情
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"获取消息详情失败：{result.get('msg')}")
```

### 4. 撤回消息

```python
def recall_message(access_token: str, message_id: str) -> bool:
    """
    撤回消息
    
    Args:
        access_token: Access Token
        message_id: 消息 ID
    
    Returns:
        bool: 撤回是否成功
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/recall"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.post(url, headers=headers, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 5. 创建群组

```python
def create_chat(access_token: str,
               name: str,
               owner_id: str,
               user_ids: Optional[List[str]] = None,
               description: Optional[str] = None) -> str:
    """
    创建群组
    
    Args:
        access_token: Access Token
        name: 群名称
        owner_id: 群主 ID
        user_ids: 初始成员列表（可选）
        description: 群描述（可选）
    
    Returns:
        str: 群聊 ID
    """
    url = "https://open.feishu.cn/open-apis/im/v1/chats"
    
    payload = {
        "name": name,
        "owner_id": owner_id
    }
    
    if user_ids:
        payload["user_ids"] = user_ids
    
    if description:
        payload["description"] = description
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["chat_id"]
    else:
        raise Exception(f"创建群组失败：{result.get('msg')}")
```

### 6. 获取群组详情

```python
def get_chat_detail(access_token: str, chat_id: str) -> Dict:
    """
    获取群组详情
    
    Args:
        access_token: Access Token
        chat_id: 群聊 ID
    
    Returns:
        dict: 群组详情
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"获取群组详情失败：{result.get('msg')}")
```

### 7. 添加群成员

```python
def add_chat_members(access_token: str, chat_id: str,
                    user_ids: List[str]) -> bool:
    """
    添加群成员
    
    Args:
        access_token: Access Token
        chat_id: 群聊 ID
        user_ids: 用户 ID 列表
    
    Returns:
        bool: 添加是否成功
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members"
    
    payload = {"user_ids": user_ids}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 8. 移除群成员

```python
def remove_chat_members(access_token: str, chat_id: str,
                       user_ids: List[str]) -> bool:
    """
    移除群成员
    
    Args:
        access_token: Access Token
        chat_id: 群聊 ID
        user_ids: 用户 ID 列表
    
    Returns:
        bool: 移除是否成功
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members"
    
    payload = {"user_ids": user_ids}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 9. 获取群成员列表

```python
def get_chat_members(access_token: str, chat_id: str,
                    page_size: int = 100) -> list:
    """
    获取群成员列表
    
    Args:
        access_token: Access Token
        chat_id: 群聊 ID
        page_size: 每页数量
    
    Returns:
        list: 成员列表
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members"
    params = {"page_size": page_size}
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取群成员列表失败：{result.get('msg')}")
```

### 10. 查询消息已读未读

```python
def get_message_read_status(access_token: str, message_id: str) -> Dict:
    """
    查询消息已读未读状态
    
    Args:
        access_token: Access Token
        message_id: 消息 ID
    
    Returns:
        dict: 已读未读状态
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/read_status"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"查询消息状态失败：{result.get('msg')}")
```

---

## 📝 实战项目：即时通讯管理系统

### 完整实现代码

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书即时通讯管理系统
Feishu Instant Messaging Management System

功能:
- 发送消息（单聊/群聊）
- 查询消息列表
- 消息撤回
- 创建群组
- 管理群成员
- 查询已读未读

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class IMManager:
    """即时通讯管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化即时通讯管理器
        
        Args:
            app_id: 应用 ID
            app_secret: 应用 Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/im/v1"
    
    def get_access_token(self) -> str:
        """获取 Access Token"""
        if self.access_token:
            return self.access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
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
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    # ========== 消息管理 ==========
    
    def send_message(self, receive_id: str, content: str,
                    msg_type: str = "text",
                    chat_type: str = "user") -> str:
        """
        发送消息
        
        Args:
            receive_id: 接收者 ID
            content: 消息内容
            msg_type: 消息类型
            chat_type: 聊天类型 (user/group)
        
        Returns:
            str: 消息 ID
        """
        url = f"{self.base_url}/messages"
        params = {"receive_id_type": chat_type}
        
        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content
        }
        
        response = requests.post(url, headers=self._get_headers(), params=params, json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["message_id"]
        else:
            raise Exception(f"发送消息失败：{result.get('msg')}")
    
    def get_message_list(self, chat_id: str, page_size: int = 20) -> List[Dict]:
        """获取消息列表"""
        url = f"{self.base_url}/messages"
        params = {
            "chat_id": chat_id,
            "page_size": page_size
        }
        
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取消息列表失败：{result.get('msg')}")
    
    def get_message_detail(self, message_id: str) -> Dict:
        """获取消息详情"""
        url = f"{self.base_url}/messages/{message_id}"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取消息详情失败：{result.get('msg')}")
    
    def recall_message(self, message_id: str) -> bool:
        """撤回消息"""
        url = f"{self.base_url}/messages/{message_id}/recall"
        
        response = requests.post(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    # ========== 群组管理 ==========
    
    def create_chat(self, name: str, owner_id: str,
                   user_ids: Optional[List[str]] = None,
                   description: Optional[str] = None) -> str:
        """
        创建群组
        
        Args:
            name: 群名称
            owner_id: 群主 ID
            user_ids: 初始成员列表
            description: 群描述
        
        Returns:
            str: 群聊 ID
        """
        url = f"{self.base_url}/chats"
        
        payload = {
            "name": name,
            "owner_id": owner_id
        }
        
        if user_ids:
            payload["user_ids"] = user_ids
        
        if description:
            payload["description"] = description
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["chat_id"]
        else:
            raise Exception(f"创建群组失败：{result.get('msg')}")
    
    def get_chat_detail(self, chat_id: str) -> Dict:
        """获取群组详情"""
        url = f"{self.base_url}/chats/{chat_id}"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取群组详情失败：{result.get('msg')}")
    
    def add_chat_members(self, chat_id: str, user_ids: List[str]) -> bool:
        """添加群成员"""
        url = f"{self.base_url}/chats/{chat_id}/members"
        
        payload = {"user_ids": user_ids}
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    def remove_chat_members(self, chat_id: str, user_ids: List[str]) -> bool:
        """移除群成员"""
        url = f"{self.base_url}/chats/{chat_id}/members"
        
        payload = {"user_ids": user_ids}
        
        response = requests.delete(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
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
    
    # ========== 消息状态 ==========
    
    def get_message_read_status(self, message_id: str) -> Dict:
        """查询消息已读未读状态"""
        url = f"{self.base_url}/messages/{message_id}/read_status"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"查询消息状态失败：{result.get('msg')}")

# ========== 命令行接口 ==========

def main():
    """主函数"""
    print("=" * 60)
    print("飞书即时通讯管理系统 v1.0")
    print("=" * 60)
    print()
    
    # 初始化
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = IMManager(app_id, app_secret)
    
    # 菜单
    while True:
        print("\n请选择操作:")
        print("1. 发送消息")
        print("2. 查询消息列表")
        print("3. 获取消息详情")
        print("4. 撤回消息")
        print("5. 创建群组")
        print("6. 获取群组详情")
        print("7. 添加群成员")
        print("8. 移除群成员")
        print("9. 获取群成员列表")
        print("10. 查询消息已读未读")
        print("11. 退出")
        print()
        
        choice = input("请输入选项 (1-11): ").strip()
        
        try:
            if choice == "1":
                receive_id = input("接收者 ID: ").strip()
                chat_type = input("聊天类型 (user/group，默认 user): ").strip() or "user"
                msg_type = input("消息类型 (text/post，默认 text): ").strip() or "text"
                content = input("消息内容：").strip()
                if msg_type == "post":
                    content = json.loads(content)
                    content = json.dumps(content)
                message_id = manager.send_message(receive_id, content, msg_type, chat_type)
                print(f"✅ 消息发送成功：{message_id}")
            
            elif choice == "2":
                chat_id = input("群聊 ID: ").strip()
                messages = manager.get_message_list(chat_id)
                print(f"\n共 {len(messages)} 条消息:")
                for msg in messages[:10]:
                    print(f"  - {msg.get('content')[:50]}... (from: {msg.get('sender_id')})")
            
            elif choice == "3":
                message_id = input("消息 ID: ").strip()
                msg = manager.get_message_detail(message_id)
                print(f"\n消息详情:")
                print(f"  内容：{msg.get('content')}")
                print(f"  发送人：{msg.get('sender_id')}")
                print(f"  时间：{msg.get('create_time')}")
            
            elif choice == "4":
                message_id = input("消息 ID: ").strip()
                success = manager.recall_message(message_id)
                print("✅ 撤回成功" if success else "❌ 撤回失败")
            
            elif choice == "5":
                name = input("群名称：").strip()
                owner_id = input("群主 ID: ").strip()
                members = input("初始成员（逗号分隔，可选）: ").strip()
                member_list = [x.strip() for x in members.split(",")] if members else None
                chat_id = manager.create_chat(name, owner_id, member_list)
                print(f"✅ 群组创建成功：{chat_id}")
            
            elif choice == "6":
                chat_id = input("群聊 ID: ").strip()
                chat = manager.get_chat_detail(chat_id)
                print(f"\n群组详情:")
                print(f"  名称：{chat.get('name')}")
                print(f"  群主：{chat.get('owner_id')}")
                print(f"  成员数：{chat.get('member_count')}")
            
            elif choice == "7":
                chat_id = input("群聊 ID: ").strip()
                user_ids = input("用户 ID 列表（逗号分隔）: ").strip().split(",")
                success = manager.add_chat_members(chat_id, [x.strip() for x in user_ids])
                print("✅ 添加成功" if success else "❌ 添加失败")
            
            elif choice == "8":
                chat_id = input("群聊 ID: ").strip()
                user_ids = input("用户 ID 列表（逗号分隔）: ").strip().split(",")
                success = manager.remove_chat_members(chat_id, [x.strip() for x in user_ids])
                print("✅ 移除成功" if success else "❌ 移除失败")
            
            elif choice == "9":
                chat_id = input("群聊 ID: ").strip()
                members = manager.get_chat_members(chat_id)
                print(f"\n共 {len(members)} 个成员:")
                for member in members[:20]:
                    print(f"  - {member.get('user_id')}")
            
            elif choice == "10":
                message_id = input("消息 ID: ").strip()
                status = manager.get_message_read_status(message_id)
                print(f"\n已读状态:")
                print(f"  已读数：{status.get('read_count')}")
                print(f"  未读数：{status.get('unread_count')}")
            
            elif choice == "11":
                print("再见！")
                break
            
            else:
                print("无效选项")
        
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()

```

---

## ⚠️ 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 0 | 成功 | - |
| 99991663 | Token 无效 | 重新获取 Token |
| 99991665 | 没有权限 | 检查应用权限 |
| 99991666 | 参数错误 | 检查请求参数 |
| 60001 | 消息不存在 | 检查 message_id |
| 60002 | 消息已撤回 | 无法重复撤回 |
| 60003 | 群组不存在 | 检查 chat_id |
| 60004 | 用户不在群中 | 检查成员关系 |

---

## 📚 学习资源

### 官方文档

- 即时通讯 API: https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 消息发送：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 群组管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L3-L4

💬 **即时通讯 API 完整指南已创建！包含完整实现代码和实战项目！**

## 參考

- [[Feishu Evolution 20260413]]
- [[Asset07 Api Batch Optimize]]
