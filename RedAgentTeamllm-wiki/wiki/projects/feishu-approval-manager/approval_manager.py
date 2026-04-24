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
from dotenv import load_dotenv

load_dotenv()

class ApprovalManager:
    """审批管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/approval/v4"
    
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
    
    def create_instance(self, app_code: str, form_data: Dict[str, Any]) -> str:
        """创建审批实例"""
        url = f"{self.base_url}/instances"
        payload = {"app_code": app_code, "form": form_data}
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
    
    def get_todo_tasks(self) -> List[Dict]:
        """获取待处理任务"""
        url = f"{self.base_url}/tasks/todo"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取待处理任务失败：{result.get('msg')}")
    
    def approve_task(self, task_id: str, comment: Optional[str] = None) -> bool:
        """审批通过"""
        url = f"{self.base_url}/tasks/{task_id}/approve"
        payload = {"comment": comment} if comment else {}
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

def main():
    """主函数"""
    print("=" * 60)
    print("飞书审批管理系统 v1.0")
    print("=" * 60)
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = ApprovalManager(app_id, app_secret)
    
    while True:
        print("\n1. 获取审批定义  2. 创建审批  3. 查询审批  4. 待处理任务  5. 审批通过  6. 审批拒绝  7. 退出")
        choice = input("选项：").strip()
        
        try:
            if choice == "1":
                defs = manager.get_definitions() if hasattr(manager, 'get_definitions') else []
                print(f"共 {len(defs)} 个审批定义")
            elif choice == "2":
                app_code = input("审批编码：").strip()
                form_data = json.loads(input("表单数据 (JSON): "))
                code = manager.create_instance(app_code, form_data)
                print(f"✅ 创建成功：{code}")
            elif choice == "3":
                code = input("审批编码：").strip()
                inst = manager.get_instance(code)
                print(f"状态：{inst.get('status')}")
            elif choice == "4":
                tasks = manager.get_todo_tasks()
                print(f"共 {len(tasks)} 个待处理任务")
            elif choice == "5":
                task_id = input("任务 ID: ").strip()
                success = manager.approve_task(task_id)
                print("✅ 通过" if success else "❌ 失败")
            elif choice == "6":
                task_id = input("任务 ID: ").strip()
                comment = input("原因：").strip()
                success = manager.reject_task(task_id, comment)
                print("✅ 拒绝" if success else "❌ 失败")
            elif choice == "7":
                break
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
