#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书邮件管理系统
Feishu Email Management System

功能:
- 发送邮件
- 查询邮件列表
- 获取邮件详情
- 删除邮件
- 草稿管理

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import requests
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

class EmailManager:
    """邮件管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/mail/v1"
    
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
    
    def send_email(self, to: List[str], subject: str, content: str,
                  content_type: str = "text/plain") -> str:
        """发送邮件"""
        url = f"{self.base_url}/messages"
        payload = {"to": to, "subject": subject, "content": content, "content_type": content_type}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["message_id"]
        else:
            raise Exception(f"发送邮件失败：{result.get('msg')}")
    
    def get_email_list(self, page_size: int = 50) -> List[Dict]:
        """获取邮件列表"""
        url = f"{self.base_url}/messages"
        params = {"page_size": page_size}
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取邮件列表失败：{result.get('msg')}")
    
    def get_email_detail(self, message_id: str) -> Dict:
        """获取邮件详情"""
        url = f"{self.base_url}/messages/{message_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]
        else:
            raise Exception(f"获取邮件详情失败：{result.get('msg')}")
    
    def delete_email(self, message_id: str) -> bool:
        """删除邮件"""
        url = f"{self.base_url}/messages/{message_id}"
        response = requests.delete(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        return result.get("code") == 0
    
    def create_draft(self, to: List[str], subject: str, content: str) -> str:
        """创建草稿"""
        url = f"{self.base_url}/drafts"
        payload = {"to": to, "subject": subject, "content": content}
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result["data"]["draft_id"]
        else:
            raise Exception(f"创建草稿失败：{result.get('msg')}")
    
    def send_draft(self, draft_id: str) -> bool:
        """发送草稿"""
        url = f"{self.base_url}/drafts/{draft_id}/send"
        response = requests.post(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        return result.get("code") == 0

def main():
    """主函数"""
    print("=" * 60)
    print("飞书邮件管理系统 v1.0")
    print("=" * 60)
    
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = EmailManager(app_id, app_secret)
    
    while True:
        print("\n1. 发送邮件  2. 查询邮件  3. 获取详情  4. 删除邮件  5. 创建草稿  6. 发送草稿  7. 退出")
        choice = input("选项：").strip()
        
        try:
            if choice == "1":
                to = input("收件人：").strip().split(",")
                subject = input("主题：").strip()
                content = input("内容：").strip()
                message_id = manager.send_email(to, subject, content)
                print(f"✅ 发送成功：{message_id}")
            elif choice == "2":
                emails = manager.get_email_list()
                print(f"共 {len(emails)} 封邮件")
            elif choice == "3":
                message_id = input("邮件 ID: ").strip()
                email = manager.get_email_detail(message_id)
                print(f"主题：{email.get('subject')}")
            elif choice == "4":
                message_id = input("邮件 ID: ").strip()
                success = manager.delete_email(message_id)
                print("✅ 删除" if success else "❌ 失败")
            elif choice == "5":
                to = input("收件人：").strip().split(",")
                subject = input("主题：").strip()
                content = input("内容：").strip()
                draft_id = manager.create_draft(to, subject, content)
                print(f"✅ 草稿创建：{draft_id}")
            elif choice == "6":
                draft_id = input("草稿 ID: ").strip()
                success = manager.send_draft(draft_id)
                print("✅ 发送" if success else "❌ 失败")
            elif choice == "7":
                break
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == "__main__":
    main()
