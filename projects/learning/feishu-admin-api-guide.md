# 🏢 行政管理 API 完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L3-L4

---

## 📋 行政管理 API 概述

### 什么是行政管理 API

```
飞书行政管理 API 提供了完整的企业管理能力，包括：
- 考勤管理（打卡记录/考勤统计）
- 请假申请（创建/查询/审批）
- 报销管理（创建/查询/审批）
- 会议室预订（查询/预订/取消）
- 办公用品管理
- 班车管理
```

### 核心概念

```
考勤 (Attendance):
- 员工打卡记录
- 考勤统计报表
- 迟到/早退/缺勤统计

请假 (Leave):
- 请假申请
- 请假审批流程
- 请假类型（年假/病假/事假等）

报销 (Reimbursement):
- 报销申请
- 报销审批流程
- 报销类别

会议室 (Meeting Room):
- 会议室查询
- 会议室预订
- 预订取消

办公用品 (Office Supplies):
- 用品申请
- 用品库存管理
- 领用记录

班车 (Shuttle Bus):
- 班车路线查询
- 班车预订
- 乘车记录
```

### API 权限

```
需要的权限:
✅ admin:attendance (考勤管理)
✅ admin:leave (请假管理)
✅ admin:reimbursement (报销管理)
✅ admin:room (会议室管理)
```

---

## 🛠️ 核心 API 详解

### 1. 获取考勤记录

```python
import requests
from typing import Dict, Any, Optional, List

def get_attendance_records(access_token: str,
                          user_ids: List[str],
                          start_date: str,
                          end_date: str) -> list:
    """
    获取考勤记录
    
    Args:
        access_token: Access Token
        user_ids: 用户 ID 列表
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
    
    Returns:
        list: 考勤记录列表
    
    Example:
        >>> records = get_attendance_records(
        ...     token,
        ...     ["user_id_1", "user_id_2"],
        ...     "2026-03-01",
        ...     "2026-03-31"
        ... )
    """
    url = "https://open.feishu.cn/open-apis/workflow/v1/attendances"
    
    payload = {
        "user_ids": user_ids,
        "start_date": start_date,
        "end_date": end_date
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取考勤记录失败：{result.get('msg')}")
```

### 2. 获取考勤统计

```python
def get_attendance_stats(access_token: str,
                        department_id: str,
                        month: str) -> Dict:
    """
    获取考勤统计
    
    Args:
        access_token: Access Token
        department_id: 部门 ID
        month: 月份 (YYYY-MM)
    
    Returns:
        dict: 考勤统计信息
    """
    url = "https://open.feishu.cn/open-apis/workflow/v1/attendances/stats"
    
    payload = {
        "department_id": department_id,
        "month": month
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
        raise Exception(f"获取考勤统计失败：{result.get('msg')}")
```

### 3. 创建请假申请

```python
def create_leave_request(access_token: str,
                        user_id: str,
                        leave_type: str,
                        start_time: str,
                        end_time: str,
                        reason: Optional[str] = None) -> str:
    """
    创建请假申请
    
    Args:
        access_token: Access Token
        user_id: 用户 ID
        leave_type: 请假类型 (annual/sick/personal 等)
        start_time: 开始时间 (ISO 8601)
        end_time: 结束时间 (ISO 8601)
        reason: 请假原因
    
    Returns:
        str: 请假申请 ID
    
    Example:
        >>> leave_id = create_leave_request(
        ...     token,
        ...     "user_id",
        ...     "annual",
        ...     "2026-03-20T09:00:00+08:00",
        ...     "2026-03-22T18:00:00+08:00",
        ...     "年假休息"
        ... )
    """
    url = "https://open.feishu.cn/open-apis/workflow/v1/leaves"
    
    payload = {
        "user_id": user_id,
        "leave_type": leave_type,
        "start_time": start_time,
        "end_time": end_time
    }
    
    if reason:
        payload["reason"] = reason
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["leave_id"]
    else:
        raise Exception(f"创建请假申请失败：{result.get('msg')}")
```

### 4. 查询请假申请

```python
def get_leave_request(access_token: str, leave_id: str) -> Dict:
    """
    查询请假申请
    
    Args:
        access_token: Access Token
        leave_id: 请假申请 ID
    
    Returns:
        dict: 请假申请详情
    """
    url = f"https://open.feishu.cn/open-apis/workflow/v1/leaves/{leave_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"查询请假申请失败：{result.get('msg')}")
```

### 5. 获取请假类型列表

```python
def get_leave_types(access_token: str) -> list:
    """
    获取请假类型列表
    
    Args:
        access_token: Access Token
    
    Returns:
        list: 请假类型列表
    """
    url = "https://open.feishu.cn/open-apis/workflow/v1/leave_types"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取请假类型失败：{result.get('msg')}")
```

### 6. 创建报销申请

```python
def create_reimbursement(access_token: str,
                        user_id: str,
                        amount: float,
                        category: str,
                        description: str,
                        receipts: Optional[List[str]] = None) -> str:
    """
    创建报销申请
    
    Args:
        access_token: Access Token
        user_id: 用户 ID
        amount: 报销金额
        category: 报销类别
        description: 报销说明
        receipts: 收据图片 ID 列表
    
    Returns:
        str: 报销申请 ID
    """
    url = "https://open.feishu.cn/open-apis/workflow/v1/reimbursements"
    
    payload = {
        "user_id": user_id,
        "amount": amount,
        "category": category,
        "description": description
    }
    
    if receipts:
        payload["receipts"] = receipts
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["reimbursement_id"]
    else:
        raise Exception(f"创建报销申请失败：{result.get('msg')}")
```

### 7. 查询会议室列表

```python
def get_meeting_rooms(access_token: str,
                     building_id: Optional[str] = None,
                     capacity: Optional[int] = None) -> list:
    """
    查询会议室列表
    
    Args:
        access_token: Access Token
        building_id: 楼栋 ID（可选）
        capacity: 最小容纳人数（可选）
    
    Returns:
        list: 会议室列表
    """
    url = "https://open.feishu.cn/open-apis/workflow/v1/rooms"
    params = {}
    
    if building_id:
        params["building_id"] = building_id
    
    if capacity:
        params["capacity"] = capacity
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"查询会议室失败：{result.get('msg')}")
```

### 8. 预订会议室

```python
def book_meeting_room(access_token: str,
                     room_id: str,
                     user_id: str,
                     start_time: str,
                     end_time: str,
                     title: Optional[str] = None) -> str:
    """
    预订会议室
    
    Args:
        access_token: Access Token
        room_id: 会议室 ID
        user_id: 预订人 ID
        start_time: 开始时间 (ISO 8601)
        end_time: 结束时间 (ISO 8601)
        title: 会议标题
    
    Returns:
        str: 预订 ID
    """
    url = "https://open.feishu.cn/open-apis/workflow/v1/rooms/reservations"
    
    payload = {
        "room_id": room_id,
        "user_id": user_id,
        "start_time": start_time,
        "end_time": end_time
    }
    
    if title:
        payload["title"] = title
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["reservation_id"]
    else:
        raise Exception(f"预订会议室失败：{result.get('msg')}")
```

### 9. 取消会议室预订

```python
def cancel_meeting_room(access_token: str, reservation_id: str) -> bool:
    """
    取消会议室预订
    
    Args:
        access_token: Access Token
        reservation_id: 预订 ID
    
    Returns:
        bool: 取消是否成功
    """
    url = f"https://open.feishu.cn/open-apis/workflow/v1/rooms/reservations/{reservation_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(url, headers=headers, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

---

## 📝 实战项目：行政管理系统

### 完整实现代码

```python
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
import json
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AdminManager:
    """行政管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化行政管理器
        
        Args:
            app_id: 应用 ID
            app_secret: 应用 Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/workflow/v1"
    
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
    
    # ========== 考勤管理 ==========
    
    def get_attendance_records(self, user_ids: List[str],
                              start_date: str, end_date: str) -> List[Dict]:
        """获取考勤记录"""
        url = f"{self.base_url}/attendances"
        
        payload = {
            "user_ids": user_ids,
            "start_date": start_date,
            "end_date": end_date
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取考勤记录失败：{result.get('msg')}")
    
    def get_attendance_stats(self, department_id: str, month: str) -> Dict:
        """获取考勤统计"""
        url = f"{self.base_url}/attendances/stats"
        
        payload = {
            "department_id": department_id,
            "month": month
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取考勤统计失败：{result.get('msg')}")
    
    # ========== 请假管理 ==========
    
    def create_leave_request(self, user_id: str, leave_type: str,
                            start_time: str, end_time: str,
                            reason: Optional[str] = None) -> str:
        """创建请假申请"""
        url = f"{self.base_url}/leaves"
        
        payload = {
            "user_id": user_id,
            "leave_type": leave_type,
            "start_time": start_time,
            "end_time": end_time
        }
        
        if reason:
            payload["reason"] = reason
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["leave_id"]
        else:
            raise Exception(f"创建请假申请失败：{result.get('msg')}")
    
    def get_leave_request(self, leave_id: str) -> Dict:
        """查询请假申请"""
        url = f"{self.base_url}/leaves/{leave_id}"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"查询请假申请失败：{result.get('msg')}")
    
    def get_leave_types(self) -> List[Dict]:
        """获取请假类型列表"""
        url = f"{self.base_url}/leave_types"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取请假类型失败：{result.get('msg')}")
    
    # ========== 报销管理 ==========
    
    def create_reimbursement(self, user_id: str, amount: float,
                            category: str, description: str) -> str:
        """创建报销申请"""
        url = f"{self.base_url}/reimbursements"
        
        payload = {
            "user_id": user_id,
            "amount": amount,
            "category": category,
            "description": description
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["reimbursement_id"]
        else:
            raise Exception(f"创建报销申请失败：{result.get('msg')}")
    
    # ========== 会议室管理 ==========
    
    def get_meeting_rooms(self, building_id: Optional[str] = None,
                         capacity: Optional[int] = None) -> List[Dict]:
        """查询会议室列表"""
        url = f"{self.base_url}/rooms"
        params = {}
        
        if building_id:
            params["building_id"] = building_id
        
        if capacity:
            params["capacity"] = capacity
        
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"查询会议室失败：{result.get('msg')}")
    
    def book_meeting_room(self, room_id: str, user_id: str,
                         start_time: str, end_time: str,
                         title: Optional[str] = None) -> str:
        """预订会议室"""
        url = f"{self.base_url}/rooms/reservations"
        
        payload = {
            "room_id": room_id,
            "user_id": user_id,
            "start_time": start_time,
            "end_time": end_time
        }
        
        if title:
            payload["title"] = title
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["reservation_id"]
        else:
            raise Exception(f"预订会议室失败：{result.get('msg')}")
    
    def cancel_meeting_room(self, reservation_id: str) -> bool:
        """取消会议室预订"""
        url = f"{self.base_url}/rooms/reservations/{reservation_id}"
        
        response = requests.delete(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        return result.get("code") == 0

# ========== 命令行接口 ==========

def main():
    """主函数"""
    print("=" * 60)
    print("飞书行政管理系统 v1.0")
    print("=" * 60)
    print()
    
    # 初始化
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = AdminManager(app_id, app_secret)
    
    # 菜单
    while True:
        print("\n请选择操作:")
        print("1. 获取考勤记录")
        print("2. 获取考勤统计")
        print("3. 创建请假申请")
        print("4. 查询请假申请")
        print("5. 获取请假类型")
        print("6. 创建报销申请")
        print("7. 查询会议室")
        print("8. 预订会议室")
        print("9. 取消会议室预订")
        print("10. 退出")
        print()
        
        choice = input("请输入选项 (1-10): ").strip()
        
        try:
            if choice == "1":
                user_ids = input("用户 ID 列表（逗号分隔）: ").strip().split(",")
                start_date = input("开始日期 (YYYY-MM-DD): ").strip()
                end_date = input("结束日期 (YYYY-MM-DD): ").strip()
                records = manager.get_attendance_records([x.strip() for x in user_ids], start_date, end_date)
                print(f"\n共 {len(records)} 条考勤记录")
            
            elif choice == "2":
                dept_id = input("部门 ID: ").strip()
                month = input("月份 (YYYY-MM): ").strip()
                stats = manager.get_attendance_stats(dept_id, month)
                print(f"\n考勤统计:")
                print(f"  应到：{stats.get('expected_count')}")
                print(f"  实到：{stats.get('actual_count')}")
            
            elif choice == "3":
                user_id = input("用户 ID: ").strip()
                leave_types = manager.get_leave_types()
                print("\n请假类型:")
                for lt in leave_types:
                    print(f"  - {lt.get('name')} ({lt.get('type')})")
                leave_type = input("请假类型：").strip()
                start_time = input("开始时间 (ISO 8601): ").strip()
                end_time = input("结束时间 (ISO 8601): ").strip()
                reason = input("请假原因：").strip()
                leave_id = manager.create_leave_request(user_id, leave_type, start_time, end_time, reason)
                print(f"✅ 请假申请创建成功：{leave_id}")
            
            elif choice == "4":
                leave_id = input("请假申请 ID: ").strip()
                leave = manager.get_leave_request(leave_id)
                print(f"\n请假申请详情:")
                print(f"  状态：{leave.get('status')}")
                print(f"  类型：{leave.get('leave_type')}")
                print(f"  时间：{leave.get('start_time')} - {leave.get('end_time')}")
            
            elif choice == "5":
                leave_types = manager.get_leave_types()
                print(f"\n共 {len(leave_types)} 个请假类型:")
                for lt in leave_types:
                    print(f"  - {lt.get('name')}")
            
            elif choice == "6":
                user_id = input("用户 ID: ").strip()
                amount = float(input("报销金额：").strip())
                category = input("报销类别：").strip()
                description = input("报销说明：").strip()
                reimbursement_id = manager.create_reimbursement(user_id, amount, category, description)
                print(f"✅ 报销申请创建成功：{reimbursement_id}")
            
            elif choice == "7":
                rooms = manager.get_meeting_rooms()
                print(f"\n共 {len(rooms)} 个会议室:")
                for room in rooms:
                    print(f"  - {room.get('name')} (容纳：{room.get('capacity')}人)")
            
            elif choice == "8":
                rooms = manager.get_meeting_rooms()
                room_id = input("会议室 ID: ").strip()
                user_id = input("预订人 ID: ").strip()
                start_time = input("开始时间 (ISO 8601): ").strip()
                end_time = input("结束时间 (ISO 8601): ").strip()
                title = input("会议标题（可选）: ").strip() or None
                reservation_id = manager.book_meeting_room(room_id, user_id, start_time, end_time, title)
                print(f"✅ 会议室预订成功：{reservation_id}")
            
            elif choice == "9":
                reservation_id = input("预订 ID: ").strip()
                success = manager.cancel_meeting_room(reservation_id)
                print("✅ 取消成功" if success else "❌ 取消失败")
            
            elif choice == "10":
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
| 80001 | 考勤记录不存在 | 检查日期范围 |
| 80002 | 请假类型无效 | 检查 leave_type |
| 80003 | 会议室已被预订 | 选择其他时间或会议室 |

---

## 📚 学习资源

### 官方文档

- 行政管理 API: https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 考勤管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 请假管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L3-L4

🏢 **行政管理 API 完整指南已创建！包含完整实现代码和实战项目！**
