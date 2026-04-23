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
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis"
    
    def get_access_token(self) -> str:
        """获取 Access Token"""
        if self.access_token:
            return self.access_token
        
        url = f"{self.base_url}/auth/v3/app_access_token/internal"
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
    
    def add_file_permission(self, file_token: str, user_id: str, role: str = "edit") -> Dict:
        """添加文档权限"""
        url = f"{self.base_url}/drive/v1/permissions"
        payload = {"file_id": file_token, "member": {"type": "user", "user_id": user_id}, "role": role}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"添加文档权限失败：{result.get('msg')}")
    
    def batch_add_file_permissions(self, file_token: str, members: List[Dict]) -> Dict:
        """批量添加文档权限"""
        results = {"success": 0, "fail": 0, "details": []}
        for member in members:
            try:
                self.add_file_permission(file_token, member["user_id"], member.get("role", "edit"))
                results["success"] += 1
            except Exception as e:
                results["fail"] += 1
                results["details"].append({"user_id": member["user_id"], "error": str(e)})
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
    
    # ========== 权限审计 ==========
    
    def get_permission_logs(self, days: int = 7) -> List[Dict]:
        """获取权限使用记录"""
        start_time = (datetime.now() - timedelta(days=days)).isoformat()
        end_time = datetime.now().isoformat()
        url = f"{self.base_url}/audit/v1/permission_logs"
        params = {"start_time": start_time, "end_time": end_time, "page_size": 100}
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取权限记录失败：{result.get('msg')}")

def main():
    """主函数"""
    print("=" * 60)
    print("飞书权限管理系统 v1.0")
    print("=" * 60)
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = PermissionManager(app_id, app_secret)
    
    while True:
        print("\n1. 获取文档权限  2. 添加文档权限  3. 获取角色列表  4. 获取权限记录  5. 退出")
        choice = input("选项：").strip()
        
        try:
            if choice == "1":
                file_token = input("文档 Token: ").strip()
                perms = manager.get_file_permissions(file_token)
                print(f"共 {len(perms)} 个权限")
            elif choice == "2":
                file_token = input("文档 Token: ").strip()
                user_id = input("用户 ID: ").strip()
                manager.add_file_permission(file_token, user_id)
                print("✅ 权限添加成功")
            elif choice == "3":
                roles = manager.get_roles()
                print(f"共 {len(roles)} 个角色")
            elif choice == "4":
                logs = manager.get_permission_logs()
                print(f"共 {len(logs)} 条记录")
            elif choice == "5":
                break
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
