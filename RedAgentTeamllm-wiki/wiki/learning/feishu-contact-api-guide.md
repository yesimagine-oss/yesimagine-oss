---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 通讯录
- api
- 完整指南
- guide
title: Feishu Contact Api Guide
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
# 📒 通讯录 API 完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L2-L3

---

## 📋 通讯录 API 概述

### 什么是通讯录 API

```
飞书通讯录 API 提供了完整的组织架构管理能力，包括：
- 部门管理（创建/查询/更新/删除）
- 用户管理（创建/查询/更新/删除）
- 用户组管理
- 批量操作
- 通讯录事件订阅
```

### API 权限

```
需要的权限:
✅ contact:department (部门管理)
✅ contact:user (用户管理)
✅ contact:user:readonly (只读用户)
✅ contact:department:readonly (只读部门)
```

---

## 🏢 部门管理 API

### 1. 获取部门列表

```python
import requests

def get_departments(access_token: str, parent_department_id: str = "0"):
    """
    获取部门列表
    
    Args:
        access_token: Access Token
        parent_department_id: 父部门 ID（0 表示根部门）
    
    Returns:
        list: 部门列表
    """
    url = "https://open.feishu.cn/open-apis/contact/v3/departments"
    params = {
        "page_size": 100,
        "parent_department_id": parent_department_id
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取部门列表失败：{result.get('msg')}")
```

### 2. 创建部门

```python
def create_department(access_token: str, name: str, 
                     parent_department_id: str = "0",
                     leader_user_id: Optional[str] = None):
    """
    创建部门
    
    Args:
        access_token: Access Token
        name: 部门名称
        parent_department_id: 父部门 ID
        leader_user_id: 部门主管用户 ID
    
    Returns:
        dict: 创建的部门信息
    """
    url = "https://open.feishu.cn/open-apis/contact/v3/departments"
    
    payload = {
        "name": name,
        "parent_department_id": parent_department_id
    }
    
    if leader_user_id:
        payload["leader_user_id"] = leader_user_id
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["department"]
    else:
        raise Exception(f"创建部门失败：{result.get('msg')}")
```

### 3. 更新部门

```python
def update_department(access_token: str, department_id: str, **kwargs):
    """
    更新部门
    
    Args:
        access_token: Access Token
        department_id: 部门 ID
        **kwargs: 更新字段（name, leader_user_id 等）
    
    Returns:
        dict: 更新后的部门信息
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/departments/{department_id}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=kwargs)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["department"]
    else:
        raise Exception(f"更新部门失败：{result.get('msg')}")
```

### 4. 删除部门

```python
def delete_department(access_token: str, department_id: str):
    """
    删除部门
    
    Args:
        access_token: Access Token
        department_id: 部门 ID
    
    Returns:
        bool: 删除是否成功
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/departments/{department_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        return True
    else:
        raise Exception(f"删除部门失败：{result.get('msg')}")
```

---

## 👥 用户管理 API

### 1. 获取用户信息

```python
def get_user(access_token: str, user_id: str, 
            user_id_type: str = "user_id"):
    """
    获取用户信息
    
    Args:
        access_token: Access Token
        user_id: 用户 ID
        user_id_type: ID 类型 (open_id/union_id/user_id)
    
    Returns:
        dict: 用户信息
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/users/{user_id}"
    params = {"user_id_type": user_id_type}
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["user"]
    else:
        raise Exception(f"获取用户信息失败：{result.get('msg')}")
```

### 2. 创建用户

```python
def create_user(access_token: str, mobile: str, name: str,
               email: Optional[str] = None,
               department_ids: Optional[List[str]] = None):
    """
    创建用户
    
    Args:
        access_token: Access Token
        mobile: 手机号
        name: 姓名
        email: 邮箱
        department_ids: 部门 ID 列表
    
    Returns:
        dict: 创建的用户信息
    """
    url = "https://open.feishu.cn/open-apis/contact/v3/users"
    
    payload = {
        "mobile": mobile,
        "name": name
    }
    
    if email:
        payload["email"] = email
    
    if department_ids:
        payload["department_ids"] = department_ids
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["user"]
    else:
        raise Exception(f"创建用户失败：{result.get('msg')}")
```

### 3. 更新用户

```python
def update_user(access_token: str, user_id: str, **kwargs):
    """
    更新用户
    
    Args:
        access_token: Access Token
        user_id: 用户 ID
        **kwargs: 更新字段（name, email, mobile 等）
    
    Returns:
        dict: 更新后的用户信息
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/users/{user_id}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=kwargs)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["user"]
    else:
        raise Exception(f"更新用户失败：{result.get('msg')}")
```

### 4. 删除用户

```python
def delete_user(access_token: str, user_id: str):
    """
    删除用户
    
    Args:
        access_token: Access Token
        user_id: 用户 ID
    
    Returns:
        bool: 删除是否成功
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/users/{user_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        return True
    else:
        raise Exception(f"删除用户失败：{result.get('msg')}")
```

### 5. 批量获取用户

```python
def batch_get_users(access_token: str, user_ids: List[str],
                   user_id_type: str = "user_id"):
    """
    批量获取用户
    
    Args:
        access_token: Access Token
        user_ids: 用户 ID 列表
        user_id_type: ID 类型
    
    Returns:
        list: 用户列表
    """
    url = "https://open.feishu.cn/open-apis/contact/v3/users/batch"
    
    payload = {
        "user_ids": user_ids,
        "user_id_type": user_id_type
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"批量获取用户失败：{result.get('msg')}")
```

---

## 🔍 搜索与查询

### 1. 搜索用户

```python
def search_users(access_token: str, query: str, 
                page_size: int = 50):
    """
    搜索用户
    
    Args:
        access_token: Access Token
        query: 搜索关键词（姓名/手机号/邮箱）
        page_size: 每页数量
    
    Returns:
        list: 用户列表
    """
    url = "https://open.feishu.cn/open-apis/contact/v3/users/search"
    
    payload = {
        "query": query,
        "page_size": page_size
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"搜索用户失败：{result.get('msg')}")
```

### 2. 获取部门用户列表

```python
def get_department_users(access_token: str, department_id: str,
                        page_size: int = 100):
    """
    获取部门用户列表
    
    Args:
        access_token: Access Token
        department_id: 部门 ID
        page_size: 每页数量
    
    Returns:
        list: 用户列表
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/departments/{department_id}/users"
    params = {"page_size": page_size}
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取部门用户失败：{result.get('msg')}")
```

---

## 📊 实战项目：通讯录管理工具

### 完整实现代码

```python
#!/usr/bin/env python3
"""
飞书通讯录管理工具
Feishu Contact Manager

功能:
- 部门管理
- 用户管理
- 批量操作
- 搜索查询

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

class ContactManager:
    """通讯录管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化通讯录管理器
        
        Args:
            app_id: 应用 ID
            app_secret: 应用 Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.base_url = "https://open.feishu.cn/open-apis/contact/v3"
    
    def get_access_token(self) -> str:
        """获取 Access Token"""
        if self.access_token:
            return self.access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload)
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
    
    # ========== 部门管理 ==========
    
    def get_departments(self, parent_id: str = "0") -> List[Dict]:
        """获取部门列表"""
        url = f"{self.base_url}/departments"
        params = {"parent_department_id": parent_id}
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取部门列表失败：{result.get('msg')}")
    
    def create_department(self, name: str, parent_id: str = "0",
                         leader_id: Optional[str] = None) -> Dict:
        """创建部门"""
        url = f"{self.base_url}/departments"
        payload = {
            "name": name,
            "parent_department_id": parent_id
        }
        
        if leader_id:
            payload["leader_user_id"] = leader_id
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["department"]
        else:
            raise Exception(f"创建部门失败：{result.get('msg')}")
    
    def update_department(self, department_id: str, **kwargs) -> Dict:
        """更新部门"""
        url = f"{self.base_url}/departments/{department_id}"
        
        response = requests.patch(url, headers=self._get_headers(), json=kwargs)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["department"]
        else:
            raise Exception(f"更新部门失败：{result.get('msg')}")
    
    def delete_department(self, department_id: str) -> bool:
        """删除部门"""
        url = f"{self.base_url}/departments/{department_id}"
        
        response = requests.delete(url, headers=self._get_headers())
        result = response.json()
        
        return result.get("code") == 0
    
    # ========== 用户管理 ==========
    
    def get_user(self, user_id: str, id_type: str = "user_id") -> Dict:
        """获取用户信息"""
        url = f"{self.base_url}/users/{user_id}"
        params = {"user_id_type": id_type}
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["user"]
        else:
            raise Exception(f"获取用户信息失败：{result.get('msg')}")
    
    def create_user(self, mobile: str, name: str,
                   email: Optional[str] = None,
                   department_ids: Optional[List[str]] = None) -> Dict:
        """创建用户"""
        url = f"{self.base_url}/users"
        payload = {
            "mobile": mobile,
            "name": name
        }
        
        if email:
            payload["email"] = email
        
        if department_ids:
            payload["department_ids"] = department_ids
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["user"]
        else:
            raise Exception(f"创建用户失败：{result.get('msg')}")
    
    def update_user(self, user_id: str, **kwargs) -> Dict:
        """更新用户"""
        url = f"{self.base_url}/users/{user_id}"
        
        response = requests.patch(url, headers=self._get_headers(), json=kwargs)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["user"]
        else:
            raise Exception(f"更新用户失败：{result.get('msg')}")
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        url = f"{self.base_url}/users/{user_id}"
        
        response = requests.delete(url, headers=self._get_headers())
        result = response.json()
        
        return result.get("code") == 0
    
    def batch_get_users(self, user_ids: List[str]) -> List[Dict]:
        """批量获取用户"""
        url = f"{self.base_url}/users/batch"
        payload = {"user_ids": user_ids}
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"批量获取用户失败：{result.get('msg')}")
    
    def search_users(self, query: str) -> List[Dict]:
        """搜索用户"""
        url = f"{self.base_url}/users/search"
        payload = {"query": query}
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"搜索用户失败：{result.get('msg')}")
    
    def get_department_users(self, department_id: str) -> List[Dict]:
        """获取部门用户列表"""
        url = f"{self.base_url}/departments/{department_id}/users"
        
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取部门用户失败：{result.get('msg')}")

# ========== 命令行接口 ==========

def main():
    """主函数"""
    print("=" * 60)
    print("飞书通讯录管理工具 v1.0")
    print("=" * 60)
    print()
    
    # 初始化
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = ContactManager(app_id, app_secret)
    
    # 菜单
    while True:
        print("\n请选择操作:")
        print("1. 获取部门列表")
        print("2. 创建部门")
        print("3. 获取用户信息")
        print("4. 创建用户")
        print("5. 搜索用户")
        print("6. 批量获取用户")
        print("7. 获取部门用户")
        print("8. 退出")
        print()
        
        choice = input("请输入选项 (1-8): ").strip()
        
        try:
            if choice == "1":
                parent_id = input("父部门 ID (默认 0): ").strip() or "0"
                departments = manager.get_departments(parent_id)
                print(f"\n共 {len(departments)} 个部门:")
                for dept in departments:
                    print(f"  - {dept['name']} (ID: {dept['department_id']})")
            
            elif choice == "2":
                name = input("部门名称：").strip()
                parent_id = input("父部门 ID (默认 0): ").strip() or "0"
                dept = manager.create_department(name, parent_id)
                print(f"✅ 部门创建成功：{dept['name']}")
            
            elif choice == "3":
                user_id = input("用户 ID: ").strip()
                user = manager.get_user(user_id)
                print(f"\n用户信息:")
                print(f"  姓名：{user.get('name')}")
                print(f"  邮箱：{user.get('email')}")
                print(f"  手机：{user.get('mobile')}")
            
            elif choice == "4":
                mobile = input("手机号：").strip()
                name = input("姓名：").strip()
                email = input("邮箱 (可选): ").strip() or None
                user = manager.create_user(mobile, name, email)
                print(f"✅ 用户创建成功：{user['name']}")
            
            elif choice == "5":
                query = input("搜索关键词：").strip()
                users = manager.search_users(query)
                print(f"\n找到 {len(users)} 个用户:")
                for user in users:
                    print(f"  - {user['name']} ({user.get('email')})")
            
            elif choice == "6":
                user_ids = input("用户 ID 列表（逗号分隔）: ").strip().split(",")
                users = manager.batch_get_users(user_ids)
                print(f"\n共 {len(users)} 个用户:")
                for user in users:
                    print(f"  - {user['name']}")
            
            elif choice == "7":
                dept_id = input("部门 ID: ").strip()
                users = manager.get_department_users(dept_id)
                print(f"\n部门共 {len(users)} 个用户:")
                for user in users:
                    print(f"  - {user['name']}")
            
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
| 10001 | 用户已存在 | 使用不同的手机号 |
| 10002 | 部门不存在 | 检查部门 ID |
| 10003 | 用户不存在 | 检查用户 ID |

---

## 📚 学习资源

### 官方文档

- 通讯录 API: https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 部门管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 用户管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L2-L3

📒 **通讯录 API 完整指南已创建！包含完整实现代码和实战项目！**

## 參考

- [[Feishu Evolution 20260413]]


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[INSTALL-VALIDATOR-GUIDE]]
