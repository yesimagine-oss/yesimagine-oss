# ✅ 审批流 API 完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L3-L4

---

## 📋 审批流 API 概述

### 什么是审批流 API

```
飞书审批流 API 提供了完整的审批管理能力，包括：
- 创建审批实例
- 查询审批状态
- 审批通过/拒绝
- 获取审批定义
- 订阅审批事件
- 批量操作
```

### 核心概念

```
审批定义 (Approval Definition):
- 审批流程模板
- 包含审批节点、审批人等配置

审批实例 (Approval Instance):
- 根据审批定义创建的具体审批
- 包含表单数据、审批状态等

审批任务 (Approval Task):
- 审批流程中的具体任务
- 需要审批人处理

审批人 (Approver):
- 处理审批任务的用户
- 可以有多级审批人
```

### API 权限

```
需要的权限:
✅ approval:instance (审批实例管理)
✅ approval:definition (审批定义管理)
✅ approval:task (审批任务管理)
```

---

## 🛠️ 核心 API 详解

### 1. 创建审批实例

```python
import requests
from typing import Dict, Any, Optional

def create_approval_instance(access_token: str, app_code: str,
                            form_data: Dict[str, Any],
                            submitter_id: Optional[str] = None) -> str:
    """
    创建审批实例
    
    Args:
        access_token: Access Token
        app_code: 审批定义编码
        form_data: 表单数据
        submitter_id: 提交人 ID（可选，默认当前用户）
    
    Returns:
        str: 审批实例编码
    
    Example:
        >>> form_data = {
        ...     "理由": "出差申请",
        ...     "开始时间": "2026-03-20",
        ...     "结束时间": "2026-03-25",
        ...     "地点": "北京"
        ... }
        >>> instance_code = create_approval_instance(token, "leave", form_data)
    """
    url = "https://open.feishu.cn/open-apis/approval/v4/instances"
    
    payload = {
        "app_code": app_code,
        "form": form_data
    }
    
    if submitter_id:
        payload["submitter_id"] = submitter_id
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["instance_code"]
    else:
        raise Exception(f"创建审批实例失败：{result.get('msg')}")
```

### 2. 查询审批实例

```python
def get_approval_instance(access_token: str, instance_code: str) -> Dict:
    """
    查询审批实例
    
    Args:
        access_token: Access Token
        instance_code: 审批实例编码
    
    Returns:
        dict: 审批实例信息
    """
    url = f"https://open.feishu.cn/open-apis/approval/v4/instances/{instance_code}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"查询审批实例失败：{result.get('msg')}")
```

### 3. 审批通过

```python
def approve_task(access_token: str, task_id: str,
                comment: Optional[str] = None) -> bool:
    """
    审批通过
    
    Args:
        access_token: Access Token
        task_id: 审批任务 ID
        comment: 审批意见（可选）
    
    Returns:
        bool: 操作是否成功
    """
    url = f"https://open.feishu.cn/open-apis/approval/v4/tasks/{task_id}/approve"
    
    payload = {}
    if comment:
        payload["comment"] = comment
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 4. 审批拒绝

```python
def reject_task(access_token: str, task_id: str,
               comment: str) -> bool:
    """
    审批拒绝
    
    Args:
        access_token: Access Token
        task_id: 审批任务 ID
        comment: 拒绝原因（必填）
    
    Returns:
        bool: 操作是否成功
    """
    url = f"https://open.feishu.cn/open-apis/approval/v4/tasks/{task_id}/reject"
    
    payload = {"comment": comment}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 5. 获取审批定义列表

```python
def get_approval_definitions(access_token: str,
                            page_size: int = 50) -> list:
    """
    获取审批定义列表
    
    Args:
        access_token: Access Token
        page_size: 每页数量
    
    Returns:
        list: 审批定义列表
    """
    url = "https://open.feishu.cn/open-apis/approval/v4/definitions"
    params = {"page_size": page_size}
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取审批定义列表失败：{result.get('msg')}")
```

### 6. 获取待处理任务

```python
def get_pending_tasks(access_token: str,
                     page_size: int = 50) -> list:
    """
    获取待处理任务
    
    Args:
        access_token: Access Token
        page_size: 每页数量
    
    Returns:
        list: 待处理任务列表
    """
    url = "https://open.feishu.cn/open-apis/approval/v4/tasks/todo"
    params = {"page_size": page_size}
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取待处理任务失败：{result.get('msg')}")
```

---

## 📝 实战项目：审批管理系统

### 完整实现代码

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书审批管理系统
Feishu Approval Management System

功能:
- 创建审批实例
- 查询审批状态
- 审批通过/拒绝
- 获取待处理任务
- 批量操作

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import json
import time
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class ApprovalManager:
    """审批管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化审批管理器
        
        Args:
            app_id: 应用 ID
            app_secret: 应用 Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/approval/v4"
    
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
    
    # ========== 审批实例管理 ==========
    
    def create_instance(self, app_code: str, form_data: Dict[str, Any],
                       submitter_id: Optional[str] = None) -> str:
        """
        创建审批实例
        
        Args:
            app_code: 审批定义编码
            form_data: 表单数据
            submitter_id: 提交人 ID
        
        Returns:
            str: 审批实例编码
        """
        url = f"{self.base_url}/instances"
        
        payload = {
            "app_code": app_code,
            "form": form_data
        }
        
        if submitter_id:
            payload["submitter_id"] = submitter_id
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["instance_code"]
        else:
            raise Exception(f"创建审批实例失败：{result.get('msg')}")
    
    def get_instance(self, instance_code: str) -> Dict:
        """获取审批实例信息"""
        url = f"{self.base_url}/instances/{instance_code}"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取审批实例失败：{result.get('msg')}")
    
    def cancel_instance(self, instance_code: str, reason: str) -> bool:
        """取消审批实例"""
        url = f"{self.base_url}/instances/{instance_code}/cancel"
        
        payload = {"reason": reason}
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    # ========== 审批任务管理 ==========
    
    def get_todo_tasks(self, page_size: int = 50) -> List[Dict]:
        """获取待处理任务"""
        url = f"{self.base_url}/tasks/todo"
        params = {"page_size": page_size}
        
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取待处理任务失败：{result.get('msg')}")
    
    def approve_task(self, task_id: str, comment: Optional[str] = None) -> bool:
        """审批通过"""
        url = f"{self.base_url}/tasks/{task_id}/approve"
        
        payload = {}
        if comment:
            payload["comment"] = comment
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    def reject_task(self, task_id: str, comment: str) -> bool:
        """审批拒绝"""
        url = f"{self.base_url}/tasks/{task_id}/reject"
        
        payload = {"comment": comment}
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    def batch_approve(self, task_ids: List[str], comment: Optional[str] = None) -> Dict:
        """批量审批通过"""
        results = {"success": 0, "fail": 0, "details": []}
        
        for task_id in task_ids:
            try:
                success = self.approve_task(task_id, comment)
                if success:
                    results["success"] += 1
                else:
                    results["fail"] += 1
                results["details"].append({"task_id": task_id, "status": "success" if success else "fail"})
            except Exception as e:
                results["fail"] += 1
                results["details"].append({"task_id": task_id, "status": "fail", "error": str(e)})
            time.sleep(0.1)
        
        return results
    
    # ========== 审批定义管理 ==========
    
    def get_definitions(self, page_size: int = 50) -> List[Dict]:
        """获取审批定义列表"""
        url = f"{self.base_url}/definitions"
        params = {"page_size": page_size}
        
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取审批定义列表失败：{result.get('msg')}")
    
    def get_definition(self, definition_id: str) -> Dict:
        """获取审批定义详情"""
        url = f"{self.base_url}/definitions/{definition_id}"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取审批定义失败：{result.get('msg')}")

# ========== 命令行接口 ==========

def main():
    """主函数"""
    print("=" * 60)
    print("飞书审批管理系统 v1.0")
    print("=" * 60)
    print()
    
    # 初始化
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = ApprovalManager(app_id, app_secret)
    
    # 菜单
    while True:
        print("\n请选择操作:")
        print("1. 获取审批定义列表")
        print("2. 创建审批实例")
        print("3. 查询审批实例")
        print("4. 获取待处理任务")
        print("5. 审批通过")
        print("6. 审批拒绝")
        print("7. 批量审批通过")
        print("8. 退出")
        print()
        
        choice = input("请输入选项 (1-8): ").strip()
        
        try:
            if choice == "1":
                definitions = manager.get_definitions()
                print(f"\n共 {len(definitions)} 个审批定义:")
                for df in definitions:
                    print(f"  - {df.get('name')} (编码：{df.get('app_code')})")
            
            elif choice == "2":
                app_code = input("审批定义编码：").strip()
                print("输入表单数据（JSON 格式）:")
                form_data = json.loads(input())
                instance_code = manager.create_instance(app_code, form_data)
                print(f"✅ 审批实例创建成功：{instance_code}")
            
            elif choice == "3":
                instance_code = input("审批实例编码：").strip()
                instance = manager.get_instance(instance_code)
                print(f"\n审批实例信息:")
                print(f"  状态：{instance.get('status')}")
                print(f"  提交人：{instance.get('submitter')}")
                print(f"  提交时间：{instance.get('create_time')}")
            
            elif choice == "4":
                tasks = manager.get_todo_tasks()
                print(f"\n共 {len(tasks)} 个待处理任务:")
                for task in tasks:
                    print(f"  - 任务 ID: {task.get('task_id')}")
                    print(f"    审批类型：{task.get('approval_title')}")
                    print(f"    提交人：{task.get('submitter')}")
            
            elif choice == "5":
                task_id = input("任务 ID: ").strip()
                comment = input("审批意见（可选）: ").strip() or None
                success = manager.approve_task(task_id, comment)
                if success:
                    print(f"✅ 审批通过")
                else:
                    print(f"❌ 审批失败")
            
            elif choice == "6":
                task_id = input("任务 ID: ").strip()
                comment = input("拒绝原因（必填）: ").strip()
                success = manager.reject_task(task_id, comment)
                if success:
                    print(f"✅ 审批拒绝")
                else:
                    print(f"❌ 审批失败")
            
            elif choice == "7":
                task_ids = input("任务 ID 列表（逗号分隔）: ").strip().split(",")
                comment = input("审批意见（可选）: ").strip() or None
                results = manager.batch_approve(task_ids, comment)
                print(f"✅ 批量审批完成，成功 {results['success']}/{len(task_ids)} 个")
            
            elif choice == "8":
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
| 30001 | 审批定义不存在 | 检查 app_code |
| 30002 | 审批实例不存在 | 检查 instance_code |
| 30003 | 任务不存在 | 检查 task_id |
| 30004 | 任务已处理 | 无需重复处理 |

---

## 📚 学习资源

### 官方文档

- 审批流 API: https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 审批实例：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 审批任务：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L3-L4

✅ **审批流 API 完整指南已创建！包含完整实现代码和实战项目！**
