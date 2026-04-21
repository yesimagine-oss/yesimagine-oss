# 📹 视频会议 API 完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L3-L4

---

## 📋 视频会议 API 概述

### 什么是视频会议 API

```
飞书视频会议 API 提供了完整的视频会议管理能力，包括：
- 创建视频会议（即时/预约）
- 查询会议列表
- 获取会议详情
- 参会人管理
- 会议录制管理
- 会议设置
- 会议统计
```

### 核心概念

```
视频会议 (Video Meeting):
- 基于飞书会议的在线视频沟通
- 支持多人同时参与
- 支持屏幕共享、录制等功能

即时会议 (Instant Meeting):
- 立即开始的视频会议
- 无需预约
- 适合临时讨论

预约会议 (Scheduled Meeting):
- 提前预约的视频会议
- 有明确的开始/结束时间
- 适合正式会议

参会人 (Participant):
- 会议参与者
- 可以是主持人或普通参会人
- 可以设置角色

会议录制 (Recording):
- 会议视频录制
- 自动保存到云空间
- 支持回放和分享

屏幕共享 (Screen Sharing):
- 参会人可以共享屏幕
- 支持部分共享或全屏共享
```

### API 权限

```
需要的权限:
✅ meeting:meeting (会议管理)
✅ meeting:participant (参会人管理)
✅ meeting:recording (录制管理)
```

---

## 🛠️ 核心 API 详解

### 1. 创建即时视频会议

```python
import requests
from typing import Dict, Any, Optional, List

def create_instant_video_meeting(access_token: str,
                                title: str = "即时会议",
                                duration: int = 60) -> Dict[str, Any]:
    """
    创建即时视频会议
    
    Args:
        access_token: Access Token
        title: 会议标题
        duration: 会议时长（分钟）
    
    Returns:
        dict: 会议信息（包含会议号、链接等）
    
    Example:
        >>> meeting = create_instant_video_meeting(token, "项目讨论", 60)
        >>> print(f"会议号：{meeting['meeting_no']}")
        >>> print(f"链接：{meeting['meeting_url']}")
    """
    url = "https://open.feishu.cn/open-apis/mina/v1/meetings"
    
    payload = {
        "title": title,
        "duration": duration
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"创建即时视频会议失败：{result.get('msg')}")
```

### 2. 创建预约视频会议

```python
def create_scheduled_video_meeting(access_token: str,
                                  title: str,
                                  start_time: str,
                                  end_time: str,
                                  attendees: Optional[List[str]] = None,
                                  description: Optional[str] = None,
                                  settings: Optional[Dict] = None) -> str:
    """
    创建预约视频会议
    
    Args:
        access_token: Access Token
        title: 会议标题
        start_time: 开始时间 (ISO 8601 格式)
        end_time: 结束时间 (ISO 8601 格式)
        attendees: 参会人列表
        description: 会议描述
        settings: 会议设置（可选）
    
    Returns:
        str: 会议 ID
    
    Example:
        >>> meeting_id = create_scheduled_video_meeting(
        ...     token,
        ...     "项目评审会",
        ...     "2026-03-20T14:00:00+08:00",
        ...     "2026-03-20T15:00:00+08:00",
        ...     ["user_id_1", "user_id_2"]
        ... )
    """
    url = "https://open.feishu.cn/open-apis/baike/v1/meetings"
    
    payload = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time
    }
    
    if attendees:
        payload["attendees"] = attendees
    
    if description:
        payload["description"] = description
    
    if settings:
        payload["settings"] = settings
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["meeting_id"]
    else:
        raise Exception(f"创建预约视频会议失败：{result.get('msg')}")
```

### 3. 查询视频会议详情

```python
def get_video_meeting_detail(access_token: str, meeting_id: str) -> Dict:
    """
    查询视频会议详情
    
    Args:
        access_token: Access Token
        meeting_id: 会议 ID
    
    Returns:
        dict: 会议详情
    """
    url = f"https://open.feishu.cn/open-apis/baike/v1/meetings/{meeting_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"查询视频会议失败：{result.get('msg')}")
```

### 4. 更新视频会议信息

```python
def update_video_meeting(access_token: str, meeting_id: str,
                        **kwargs) -> bool:
    """
    更新视频会议信息
    
    Args:
        access_token: Access Token
        meeting_id: 会议 ID
        **kwargs: 更新字段（title/description/start_time/end_time 等）
    
    Returns:
        bool: 更新是否成功
    """
    url = f"https://open.feishu.cn/open-apis/baike/v1/meetings/{meeting_id}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=kwargs, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 5. 删除视频会议

```python
def delete_video_meeting(access_token: str, meeting_id: str) -> bool:
    """
    删除视频会议
    
    Args:
        access_token: Access Token
        meeting_id: 会议 ID
    
    Returns:
        bool: 删除是否成功
    """
    url = f"https://open.feishu.cn/open-apis/baike/v1/meetings/{meeting_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(url, headers=headers, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 6. 获取视频会议参会人列表

```python
def get_video_meeting_participants(access_token: str,
                                  meeting_id: str) -> list:
    """
    获取视频会议参会人列表
    
    Args:
        access_token: Access Token
        meeting_id: 会议 ID
    
    Returns:
        list: 参会人列表
    """
    url = f"https://open.feishu.cn/open-apis/baike/v1/meetings/{meeting_id}/attendees"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取参会人失败：{result.get('msg')}")
```

### 7. 添加视频会议参会人

```python
def add_video_meeting_participants(access_token: str, meeting_id: str,
                                  user_ids: List[str]) -> bool:
    """
    添加视频会议参会人
    
    Args:
        access_token: Access Token
        meeting_id: 会议 ID
        user_ids: 用户 ID 列表
    
    Returns:
        bool: 添加是否成功
    """
    url = f"https://open.feishu.cn/open-apis/baike/v1/meetings/{meeting_id}/attendees"
    
    payload = {"user_ids": user_ids}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 8. 获取视频会议录制

```python
def get_video_meeting_recordings(access_token: str,
                                meeting_id: str) -> list:
    """
    获取视频会议录制
    
    Args:
        access_token: Access Token
        meeting_id: 会议 ID
    
    Returns:
        list: 录制列表
    """
    url = f"https://open.feishu.cn/open-apis/baike/v1/meetings/{meeting_id}/recordings"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取会议录制失败：{result.get('msg')}")
```

### 9. 查询视频会议列表

```python
def get_video_meeting_list(access_token: str,
                          start_time: Optional[str] = None,
                          end_time: Optional[str] = None,
                          page_size: int = 50) -> list:
    """
    查询视频会议列表
    
    Args:
        access_token: Access Token
        start_time: 开始时间（可选）
        end_time: 结束时间（可选）
        page_size: 每页数量
    
    Returns:
        list: 会议列表
    """
    url = "https://open.feishu.cn/open-apis/baike/v1/meetings"
    params = {"page_size": page_size}
    
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
        raise Exception(f"查询会议列表失败：{result.get('msg')}")
```

### 10. 获取会议统计信息

```python
def get_video_meeting_stats(access_token: str,
                           meeting_id: str) -> Dict:
    """
    获取会议统计信息
    
    Args:
        access_token: Access Token
        meeting_id: 会议 ID
    
    Returns:
        dict: 会议统计信息
    """
    url = f"https://open.feishu.cn/open-apis/baike/v1/meetings/{meeting_id}/stats"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"获取会议统计失败：{result.get('msg')}")
```

---

## 📝 实战项目：视频会议管理系统

### 完整实现代码

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书视频会议管理系统
Feishu Video Meeting Management System

功能:
- 创建即时视频会议
- 创建预约视频会议
- 查询会议详情
- 更新会议信息
- 删除会议
- 管理参会人
- 获取会议录制
- 会议统计

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class VideoMeetingManager:
    """视频会议管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化视频会议管理器
        
        Args:
            app_id: 应用 ID
            app_secret: 应用 Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis"
    
    def get_access_token(self) -> str:
        """获取 Access Token"""
        if self.access_token:
            return self.access_token
        
        url = f"{self.base_url}/auth/v3/app_access_token/internal"
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
    
    # ========== 即时会议管理 ==========
    
    def create_instant_meeting(self, title: str = "即时会议",
                              duration: int = 60) -> Dict:
        """
        创建即时视频会议
        
        Args:
            title: 会议标题
            duration: 会议时长（分钟）
        
        Returns:
            dict: 会议信息
        """
        url = f"{self.base_url}/mina/v1/meetings"
        
        payload = {
            "title": title,
            "duration": duration
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"创建即时会议失败：{result.get('msg')}")
    
    # ========== 预约会议管理 ==========
    
    def create_scheduled_meeting(self, title: str, start_time: str,
                                end_time: str,
                                attendees: Optional[List[str]] = None,
                                description: Optional[str] = None,
                                settings: Optional[Dict] = None) -> str:
        """
        创建预约视频会议
        
        Args:
            title: 会议标题
            start_time: 开始时间 (ISO 8601)
            end_time: 结束时间 (ISO 8601)
            attendees: 参会人列表
            description: 会议描述
            settings: 会议设置
        
        Returns:
            str: 会议 ID
        """
        url = f"{self.base_url}/baike/v1/meetings"
        
        payload = {
            "title": title,
            "start_time": start_time,
            "end_time": end_time
        }
        
        if attendees:
            payload["attendees"] = attendees
        
        if description:
            payload["description"] = description
        
        if settings:
            payload["settings"] = settings
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["meeting_id"]
        else:
            raise Exception(f"创建预约会议失败：{result.get('msg')}")
    
    def get_meeting_detail(self, meeting_id: str) -> Dict:
        """获取会议详情"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取会议失败：{result.get('msg')}")
    
    def update_meeting(self, meeting_id: str, **kwargs) -> bool:
        """更新会议信息"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}"
        
        response = requests.patch(url, headers=self._get_headers(), json=kwargs, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    def delete_meeting(self, meeting_id: str) -> bool:
        """删除会议"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}"
        
        response = requests.delete(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    # ========== 参会人管理 ==========
    
    def get_participants(self, meeting_id: str) -> List[Dict]:
        """获取参会人列表"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}/attendees"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取参会人失败：{result.get('msg')}")
    
    def add_participants(self, meeting_id: str, user_ids: List[str]) -> bool:
        """添加参会人"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}/attendees"
        
        payload = {"user_ids": user_ids}
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    # ========== 会议录制 ==========
    
    def get_recordings(self, meeting_id: str) -> List[Dict]:
        """获取会议录制"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}/recordings"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取会议录制失败：{result.get('msg')}")
    
    # ========== 会议列表 ==========
    
    def get_meeting_list(self, start_time: Optional[str] = None,
                        end_time: Optional[str] = None,
                        page_size: int = 50) -> List[Dict]:
        """查询会议列表"""
        url = f"{self.base_url}/baike/v1/meetings"
        params = {"page_size": page_size}
        
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"查询会议列表失败：{result.get('msg')}")
    
    # ========== 会议统计 ==========
    
    def get_meeting_stats(self, meeting_id: str) -> Dict:
        """获取会议统计信息"""
        url = f"{self.base_url}/baike/v1/meetings/{meeting_id}/stats"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取会议统计失败：{result.get('msg')}")

# ========== 命令行接口 ==========

def main():
    """主函数"""
    print("=" * 60)
    print("飞书视频会议管理系统 v1.0")
    print("=" * 60)
    print()
    
    # 初始化
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = VideoMeetingManager(app_id, app_secret)
    
    # 菜单
    while True:
        print("\n请选择操作:")
        print("1. 创建即时会议")
        print("2. 创建预约会议")
        print("3. 查询会议详情")
        print("4. 更新会议")
        print("5. 删除会议")
        print("6. 获取参会人")
        print("7. 添加参会人")
        print("8. 获取会议录制")
        print("9. 查询会议列表")
        print("10. 获取会议统计")
        print("11. 退出")
        print()
        
        choice = input("请输入选项 (1-11): ").strip()
        
        try:
            if choice == "1":
                title = input("会议标题（默认"即时会议"）: ").strip() or "即时会议"
                duration = int(input("会议时长（分钟，默认 60）: ").strip() or "60")
                meeting = manager.create_instant_meeting(title, duration)
                print(f"\n✅ 即时会议创建成功!")
                print(f"  会议号：{meeting.get('meeting_no')}")
                print(f"  链接：{meeting.get('meeting_url')}")
            
            elif choice == "2":
                title = input("会议标题：").strip()
                start = input("开始时间 (YYYY-MM-DDTHH:MM:SS+08:00): ").strip()
                end = input("结束时间 (YYYY-MM-DDTHH:MM:SS+08:00): ").strip()
                attendees = input("参会人 ID 列表（逗号分隔，可选）: ").strip()
                attendees_list = [x.strip() for x in attendees.split(",")] if attendees else None
                meeting_id = manager.create_scheduled_meeting(title, start, end, attendees_list)
                print(f"✅ 预约会议创建成功：{meeting_id}")
            
            elif choice == "3":
                meeting_id = input("会议 ID: ").strip()
                meeting = manager.get_meeting_detail(meeting_id)
                print(f"\n会议详情:")
                print(f"  标题：{meeting.get('title')}")
                print(f"  状态：{meeting.get('status')}")
                print(f"  开始：{meeting.get('start_time')}")
                print(f"  结束：{meeting.get('end_time')}")
            
            elif choice == "4":
                meeting_id = input("会议 ID: ").strip()
                print("输入更新字段（JSON 格式）:")
                updates = json.loads(input())
                success = manager.update_meeting(meeting_id, **updates)
                print("✅ 更新成功" if success else "❌ 更新失败")
            
            elif choice == "5":
                meeting_id = input("会议 ID: ").strip()
                success = manager.delete_meeting(meeting_id)
                print("✅ 删除成功" if success else "❌ 删除失败")
            
            elif choice == "6":
                meeting_id = input("会议 ID: ").strip()
                participants = manager.get_participants(meeting_id)
                print(f"\n共 {len(participants)} 个参会人:")
                for p in participants:
                    print(f"  - {p.get('name')} ({p.get('user_id')})")
            
            elif choice == "7":
                meeting_id = input("会议 ID: ").strip()
                user_ids = input("用户 ID 列表（逗号分隔）: ").strip().split(",")
                success = manager.add_participants(meeting_id, [x.strip() for x in user_ids])
                print("✅ 添加成功" if success else "❌ 添加失败")
            
            elif choice == "8":
                meeting_id = input("会议 ID: ").strip()
                recordings = manager.get_recordings(meeting_id)
                print(f"\n共 {len(recordings)} 个录制:")
                for rec in recordings:
                    print(f"  - {rec.get('title')} ({rec.get('url')})")
            
            elif choice == "9":
                meetings = manager.get_meeting_list()
                print(f"\n共 {len(meetings)} 个会议:")
                for m in meetings[:10]:
                    print(f"  - {m.get('title')} ({m.get('start_time')})")
            
            elif choice == "10":
                meeting_id = input("会议 ID: ").strip()
                stats = manager.get_meeting_stats(meeting_id)
                print(f"\n会议统计:")
                print(f"  参会人数：{stats.get('participant_count')}")
                print(f"  会议时长：{stats.get('duration')}分钟")
            
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
| 70001 | 会议不存在 | 检查 meeting_id |
| 70002 | 会议已结束 | 无法操作 |
| 70003 | 参会人已存在 | 无需重复添加 |
| 70004 | 录制不存在 | 检查录制 ID |

---

## 📚 学习资源

### 官方文档

- 视频会议 API: https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 即时会议：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 预约会议：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L3-L4

📹 **视频会议 API 完整指南已创建！包含完整实现代码和实战项目！**
