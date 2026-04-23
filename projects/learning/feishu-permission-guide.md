# 🔐 权限管理完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L2-L3

---

## 📋 权限管理概述

### 什么是权限管理

```
飞书权限管理包括:
- 应用权限管理（应用能访问哪些 API）
- 文档权限管理（谁能访问哪些文档）
- 角色权限管理（用户角色和权限）
- 权限审计（权限使用记录）
```

### 权限类型

```
应用权限:
✅ contact:user (用户管理)
✅ contact:department (部门管理)
✅ message:send (消息发送)
✅ calendar:event (日历事件)
✅ drive:file (云文档)
✅ approval:instance (审批实例)
```

---

## 🏢 应用权限管理

### 1. 配置应用权限

```
步骤:
1. 访问 https://open.feishu.cn/
2. 进入应用管理
3. 选择应用 → 权限管理
4. 添加需要的权限
5. 提交审核（部分权限需要）
```

### 2. 权限分级

```
普通权限（无需审核）:
✅ contact:user:readonly
✅ contact:department:readonly
✅ message:send

需要审核的权限:
⚠️ contact:user (写权限)
⚠️ contact:department (写权限)
⚠️ drive:file (写权限)
```

---

## 📄 文档权限管理

### 1. 获取文档权限

```python
import requests

def get_file_permissions(access_token: str, file_token: str):
    """
    获取文档权限列表
    
    Args:
        access_token: Access Token
        file_token: 文件 Token
    
    Returns:
        list: 权限列表
    """
    url = f"https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/permissions"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取文档权限失败：{result.get('msg')}")
```

### 2. 添加文档权限

```python
def add_file_permission(access_token: str, file_token: str,
                       member_id: str, member_type: str = "user",
                       role: str = "edit"):
    """
    添加文档权限
    
    Args:
        access_token: Access Token
        file_token: 文件 Token
        member_id: 成员 ID
        member_type: 成员类型 (user/department)
        role: 权限角色 (view/edit/comment)
    
    Returns:
        dict: 权限信息
    """
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions"
    
    payload = {
        "file_id": file_token,
        "member": {
            "type": member_type,
            "user_id": member_id
        },
        "role": role
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"添加文档权限失败：{result.get('msg')}")
```

### 3. 更新文档权限

```python
def update_file_permission(access_token: str, file_token: str,
                          permission_id: str, role: str):
    """
    更新文档权限
    
    Args:
        access_token: Access Token
        file_token: 文件 Token
        permission_id: 权限 ID
        role: 新权限角色
    
    Returns:
        bool: 更新是否成功
    """
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{permission_id}"
    
    payload = {"role": role}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, headers=headers, json=payload)
    result = response.json()
    
    return result.get("code") == 0
```

### 4. 删除文档权限

```python
def delete_file_permission(access_token: str, permission_id: str):
    """
    删除文档权限
    
    Args:
        access_token: Access Token
        permission_id: 权限 ID
    
    Returns:
        bool: 删除是否成功
    """
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{permission_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(url, headers=headers)
    result = response.json()
    
    return result.get("code") == 0
```

### 5. 批量添加文档权限

```python
def batch_add_file_permissions(access_token: str, file_token: str,
                               members: List[Dict]):
    """
    批量添加文档权限
    
    Args:
        access_token: Access Token
        file_token: 文件 Token
        members: 成员列表 [{"user_id": "xxx", "role": "edit"}]
    
    Returns:
        dict: 添加结果
    """
    results = {"success": 0, "fail": 0, "details": []}
    
    for member in members:
        try:
            add_file_permission(
                access_token,
                file_token,
                member["user_id"],
                "user",
                member.get("role", "edit")
            )
            results["success"] += 1
            results["details"].append({
                "user_id": member["user_id"],
                "status": "success"
            })
        except Exception as e:
            results["fail"] += 1
            results["details"].append({
                "user_id": member["user_id"],
                "status": "fail",
                "error": str(e)
            })
        time.sleep(0.1)  # 避免频率限制
    
    return results
```

---

## 👥 角色权限管理

### 1. 获取角色列表

```python
def get_roles(access_token: str):
    """
    获取角色列表
    
    Args:
        access_token: Access Token
    
    Returns:
        list: 角色列表
    """
    url = "https://open.feishu.cn/open-apis/contact/v3/roles"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取角色列表失败：{result.get('msg')}")
```

### 2. 获取角色成员

```python
def get_role_users(access_token: str, role_id: str):
    """
    获取角色成员
    
    Args:
        access_token: Access Token
        role_id: 角色 ID
    
    Returns:
        list: 用户列表
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/roles/{role_id}/users"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取角色成员失败：{result.get('msg')}")
```

### 3. 添加角色成员

```python
def add_role_user(access_token: str, role_id: str, user_id: str):
    """
    添加角色成员
    
    Args:
        access_token: Access Token
        role_id: 角色 ID
        user_id: 用户 ID
    
    Returns:
        bool: 添加是否成功
    """
    url = f"https://open.feishu.cn/open-apis/contact/v3/roles/{role_id}/users"
    
    payload = {"user_ids": [user_id]}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    return result.get("code") == 0
```

---

## 📊 权限审计

### 1. 权限使用记录

```python
def get_permission_logs(access_token: str, start_time: str, end_time: str,
                       page_size: int = 100):
    """
    获取权限使用记录
    
    Args:
        access_token: Access Token
        start_time: 开始时间 (ISO 8601)
        end_time: 结束时间 (ISO 8601)
        page_size: 每页数量
    
    Returns:
        list: 权限使用记录
    """
    url = "https://open.feishu.cn/open-apis/audit/v1/permission_logs"
    
    params = {
        "start_time": start_time,
        "end_time": end_time,
        "page_size": page_size
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取权限记录失败：{result.get('msg')}")
```

### 2. 权限变更审计

```python
def get_permission_changes(access_token: str, resource_type: str,
                          resource_id: str):
    """
    获取权限变更记录
    
    Args:
        access_token: Access Token
        resource_type: 资源类型 (file/department/user)
        resource_id: 资源 ID
    
    Returns:
        list: 权限变更记录
    """
    url = "https://open.feishu.cn/open-apis/audit/v1/permission_changes"
    
    params = {
        "resource_type": resource_type,
        "resource_id": resource_id
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取权限变更记录失败：{result.get('msg')}")
```

---

## 🔐 权限设计最佳实践

### 1. 最小权限原则

```
✅ 只申请需要的权限
✅ 定期审查权限
✅ 及时撤销不用的权限
✅ 使用只读权限代替写权限

示例:
如果只需要读取用户信息:
- 申请：contact:user:readonly
- 不要申请：contact:user
```

### 2. 权限分离

```
按功能分离权限:
✅ 读权限和写权限分离
✅ 不同部门权限分离
✅ 不同角色权限分离

示例:
- 普通员工：只读权限
- 部门主管：部门写权限
- 管理员：全部权限
```

### 3. 权限审计

```
定期审计:
✅ 每周审查权限变更
✅ 每月审查权限使用
✅ 每季度审查权限配置

审计内容:
- 权限变更记录
- 权限使用记录
- 异常权限访问
```

### 4. 权限回收

```
需要回收权限的场景:
✅ 员工离职
✅ 岗位调动
✅ 项目结束
✅ 权限过期

回收流程:
1. 识别需要回收的权限
2. 备份权限记录
3. 执行权限回收
4. 验证回收结果
5. 记录回收日志
```

---

## 📝 实战项目：权限管理系统

### 完整实现代码

```python
#!/usr/bin/env python3
"""
飞书权限管理系统
Feishu Permission Manager

功能:
- 文档权限管理
- 角色权限管理
- 权限审计
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

class PermissionManager:
    """权限管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化权限管理器
        
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
    
    # ========== 文档权限管理 ==========
    
    def get_file_permissions(self, file_token: str) -> List[Dict]:
        """获取文档权限列表"""
        url = f"{self.base_url}/drive/v1/files/{file_token}/permissions"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取文档权限失败：{result.get('msg')}")
    
    def add_file_permission(self, file_token: str, user_id: str,
                           role: str = "edit") -> Dict:
        """添加文档权限"""
        url = f"{self.base_url}/drive/v1/permissions"
        
        payload = {
            "file_id": file_token,
            "member": {
                "type": "user",
                "user_id": user_id
            },
            "role": role
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"添加文档权限失败：{result.get('msg')}")
    
    def update_file_permission(self, permission_id: str, role: str) -> bool:
        """更新文档权限"""
        url = f"{self.base_url}/drive/v1/permissions/{permission_id}"
        
        payload = {"role": role}
        
        response = requests.patch(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    def delete_file_permission(self, permission_id: str) -> bool:
        """删除文档权限"""
        url = f"{self.base_url}/drive/v1/permissions/{permission_id}"
        
        response = requests.delete(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    def batch_add_file_permissions(self, file_token: str,
                                  members: List[Dict]) -> Dict:
        """批量添加文档权限"""
        results = {"success": 0, "fail": 0, "details": []}
        
        for member in members:
            try:
                self.add_file_permission(
                    file_token,
                    member["user_id"],
                    member.get("role", "edit")
                )
                results["success"] += 1
                results["details"].append({
                    "user_id": member["user_id"],
                    "status": "success"
                })
            except Exception as e:
                results["fail"] += 1
                results["details"].append({
                    "user_id": member["user_id"],
                    "status": "fail",
                    "error": str(e)
                })
            time.sleep(0.1)
        
        return results
    
    # ========== 角色权限管理 ==========
    
    def get_roles(self) -> List[Dict]:
        """获取角色列表"""
        url = f"{self.base_url}/contact/v3/roles"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取角色列表失败：{result.get('msg')}")
    
    def get_role_users(self, role_id: str) -> List[Dict]:
        """获取角色成员"""
        url = f"{self.base_url}/contact/v3/roles/{role_id}/users"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取角色成员失败：{result.get('msg')}")
    
    def add_role_user(self, role_id: str, user_id: str) -> bool:
        """添加角色成员"""
        url = f"{self.base_url}/contact/v3/roles/{role_id}/users"
        
        payload = {"user_ids": [user_id]}
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    # ========== 权限审计 ==========
    
    def get_permission_logs(self, start_time: Optional[str] = None,
                           end_time: Optional[str] = None) -> List[Dict]:
        """获取权限使用记录"""
        if not start_time:
            start_time = (datetime.now() - timedelta(days=7)).isoformat()
        if not end_time:
            end_time = datetime.now().isoformat()
        
        url = f"{self.base_url}/audit/v1/permission_logs"
        params = {
            "start_time": start_time,
            "end_time": end_time,
            "page_size": 100
        }
        
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取权限记录失败：{result.get('msg')}")
    
    def get_permission_changes(self, resource_type: str,
                              resource_id: str) -> List[Dict]:
        """获取权限变更记录"""
        url = f"{self.base_url}/audit/v1/permission_changes"
        params = {
            "resource_type": resource_type,
            "resource_id": resource_id
        }
        
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取权限变更记录失败：{result.get('msg')}")

# ========== 命令行接口 ==========

def main():
    """主函数"""
    print("=" * 60)
    print("飞书权限管理系统 v1.0")
    print("=" * 60)
    print()
    
    # 初始化
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = PermissionManager(app_id, app_secret)
    
    # 菜单
    while True:
        print("\n请选择操作:")
        print("1. 获取文档权限")
        print("2. 添加文档权限")
        print("3. 批量添加文档权限")
        print("4. 获取角色列表")
        print("5. 获取角色成员")
        print("6. 添加角色成员")
        print("7. 获取权限使用记录")
        print("8. 获取权限变更记录")
        print("9. 退出")
        print()
        
        choice = input("请输入选项 (1-9): ").strip()
        
        try:
            if choice == "1":
                file_token = input("文档 Token: ").strip()
                permissions = manager.get_file_permissions(file_token)
                print(f"\n共 {len(permissions)} 个权限:")
                for perm in permissions:
                    print(f"  - {perm.get('member', {}).get('user_id')} ({perm.get('role')})")
            
            elif choice == "2":
                file_token = input("文档 Token: ").strip()
                user_id = input("用户 ID: ").strip()
                role = input("权限角色 (view/edit/comment): ").strip() or "edit"
                manager.add_file_permission(file_token, user_id, role)
                print(f"✅ 权限添加成功")
            
            elif choice == "3":
                file_token = input("文档 Token: ").strip()
                print("输入用户 ID 列表（每行一个，空行结束）:")
                members = []
                while True:
                    user_id = input().strip()
                    if not user_id:
                        break
                    members.append({"user_id": user_id, "role": "edit"})
                
                results = manager.batch_add_file_permissions(file_token, members)
                print(f"✅ 批量添加完成，成功 {results['success']}/{len(members)} 个")
            
            elif choice == "4":
                roles = manager.get_roles()
                print(f"\n共 {len(roles)} 个角色:")
                for role in roles:
                    print(f"  - {role.get('name')} (ID: {role.get('role_id')})")
            
            elif choice == "5":
                role_id = input("角色 ID: ").strip()
                users = manager.get_role_users(role_id)
                print(f"\n角色共 {len(users)} 个成员:")
                for user in users:
                    print(f"  - {user.get('name')}")
            
            elif choice == "6":
                role_id = input("角色 ID: ").strip()
                user_id = input("用户 ID: ").strip()
                success = manager.add_role_user(role_id, user_id)
                if success:
                    print(f"✅ 角色成员添加成功")
                else:
                    print(f"❌ 添加失败")
            
            elif choice == "7":
                days = int(input("查询天数 (默认 7): ").strip() or "7")
                start_time = (datetime.now() - timedelta(days=days)).isoformat()
                logs = manager.get_permission_logs(start_time)
                print(f"\n共 {len(logs)} 条权限使用记录:")
                for log in logs[:10]:
                    print(f"  - {log.get('action')} by {log.get('user_id')}")
            
            elif choice == "8":
                resource_type = input("资源类型 (file/department/user): ").strip()
                resource_id = input("资源 ID: ").strip()
                changes = manager.get_permission_changes(resource_type, resource_id)
                print(f"\n共 {len(changes)} 条权限变更记录:")
                for change in changes[:10]:
                    print(f"  - {change.get('action')} at {change.get('time')}")
            
            elif choice == "9":
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
| 20001 | 文档不存在 | 检查文档 Token |
| 20002 | 权限已存在 | 无需重复添加 |
| 20003 | 角色不存在 | 检查角色 ID |

---

## 📚 学习资源

### 官方文档

- 权限管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 文档权限：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 角色管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L2-L3

🔐 **权限管理完整指南已创建！包含完整实现代码和实战项目！**
