# 📧 邮箱 API 完整指南

**创建时间**: 2026-03-13  
**版本**: v1.0  
**适用级别**: L3-L4

---

## 📋 邮箱 API 概述

### 什么是邮箱 API

```
飞书邮箱 API 提供了完整的邮件管理能力，包括：
- 发送邮件（文本/HTML/附件）
- 查询邮件列表
- 获取邮件详情
- 删除邮件
- 邮件标签管理
- 草稿管理
- 文件夹管理
```

### 核心概念

```
邮件 (Message):
- 邮件的基本单位
- 包含发件人、收件人、主题、内容等

邮件夹 (Folder):
- 邮件的分类容器
- 如收件箱、已发送、草稿箱等

标签 (Label):
- 邮件的标记
- 一封邮件可以有多个标签

附件 (Attachment):
- 邮件的附加文件
- 支持多种文件格式

草稿 (Draft):
- 未发送的邮件
- 可以保存后继续编辑
```

### API 权限

```
需要的权限:
✅ mail:mail (邮件管理)
✅ mail:folder (邮件夹管理)
✅ mail:label (标签管理)
✅ mail:draft (草稿管理)
```

---

## 🛠️ 核心 API 详解

### 1. 发送邮件

```python
import requests
from typing import Dict, Any, Optional, List

def send_email(access_token: str,
              to: List[str],
              subject: str,
              content: str,
              cc: Optional[List[str]] = None,
              bcc: Optional[List[str]] = None,
              content_type: str = "text/plain",
              attachments: Optional[List[str]] = None) -> str:
    """
    发送邮件
    
    Args:
        access_token: Access Token
        to: 收件人列表
        subject: 邮件主题
        content: 邮件内容
        cc: 抄送人列表（可选）
        bcc: 密送人列表（可选）
        content_type: 内容类型 (text/plain 或 text/html)
        attachments: 附件文件路径列表（可选）
    
    Returns:
        str: 邮件 ID
    
    Example:
        >>> email_id = send_email(
        ...     token,
        ...     to=["user@example.com"],
        ...     subject="项目汇报",
        ...     content="这是项目汇报内容",
        ...     content_type="text/html"
        ... )
    """
    url = "https://open.feishu.cn/open-apis/mail/v1/messages"
    
    payload = {
        "to": to,
        "subject": subject,
        "content": content,
        "content_type": content_type
    }
    
    if cc:
        payload["cc"] = cc
    
    if bcc:
        payload["bcc"] = bcc
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["message_id"]
    else:
        raise Exception(f"发送邮件失败：{result.get('msg')}")
```

### 2. 查询邮件列表

```python
def get_email_list(access_token: str,
                  folder_id: Optional[str] = None,
                  label_id: Optional[str] = None,
                  page_size: int = 50,
                  page_token: Optional[str] = None) -> list:
    """
    查询邮件列表
    
    Args:
        access_token: Access Token
        folder_id: 邮件夹 ID（可选）
        label_id: 标签 ID（可选）
        page_size: 每页数量
        page_token: 分页 token
    
    Returns:
        list: 邮件列表
    """
    url = "https://open.feishu.cn/open-apis/mail/v1/messages"
    params = {"page_size": page_size}
    
    if folder_id:
        params["folder_id"] = folder_id
    
    if label_id:
        params["label_id"] = label_id
    
    if page_token:
        params["page_token"] = page_token
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"查询邮件列表失败：{result.get('msg')}")
```

### 3. 获取邮件详情

```python
def get_email_detail(access_token: str, message_id: str) -> Dict:
    """
    获取邮件详情
    
    Args:
        access_token: Access Token
        message_id: 邮件 ID
    
    Returns:
        dict: 邮件详情
    """
    url = f"https://open.feishu.cn/open-apis/mail/v1/messages/{message_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]
    else:
        raise Exception(f"获取邮件详情失败：{result.get('msg')}")
```

### 4. 删除邮件

```python
def delete_email(access_token: str, message_id: str) -> bool:
    """
    删除邮件
    
    Args:
        access_token: Access Token
        message_id: 邮件 ID
    
    Returns:
        bool: 删除是否成功
    """
    url = f"https://open.feishu.cn/open-apis/mail/v1/messages/{message_id}"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.delete(url, headers=headers, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 5. 更新邮件标签

```python
def update_email_labels(access_token: str, message_id: str,
                       label_ids: List[str]) -> bool:
    """
    更新邮件标签
    
    Args:
        access_token: Access Token
        message_id: 邮件 ID
        label_ids: 标签 ID 列表
    
    Returns:
        bool: 更新是否成功
    """
    url = f"https://open.feishu.cn/open-apis/mail/v1/messages/{message_id}/labels"
    
    payload = {"label_ids": label_ids}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.put(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 6. 创建草稿

```python
def create_draft(access_token: str,
                to: List[str],
                subject: str,
                content: str,
                cc: Optional[List[str]] = None) -> str:
    """
    创建草稿
    
    Args:
        access_token: Access Token
        to: 收件人列表
        subject: 邮件主题
        content: 邮件内容
        cc: 抄送人列表
    
    Returns:
        str: 草稿 ID
    """
    url = "https://open.feishu.cn/open-apis/mail/v1/drafts"
    
    payload = {
        "to": to,
        "subject": subject,
        "content": content
    }
    
    if cc:
        payload["cc"] = cc
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["draft_id"]
    else:
        raise Exception(f"创建草稿失败：{result.get('msg')}")
```

### 7. 发送草稿

```python
def send_draft(access_token: str, draft_id: str) -> bool:
    """
    发送草稿
    
    Args:
        access_token: Access Token
        draft_id: 草稿 ID
    
    Returns:
        bool: 发送是否成功
    """
    url = f"https://open.feishu.cn/open-apis/mail/v1/drafts/{draft_id}/send"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.post(url, headers=headers, timeout=10)
    result = response.json()
    
    return result.get("code") == 0
```

### 8. 获取邮件夹列表

```python
def get_folders(access_token: str) -> list:
    """
    获取邮件夹列表
    
    Args:
        access_token: Access Token
    
    Returns:
        list: 邮件夹列表
    """
    url = "https://open.feishu.cn/open-apis/mail/v1/folders"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取邮件夹列表失败：{result.get('msg')}")
```

### 9. 获取标签列表

```python
def get_labels(access_token: str) -> list:
    """
    获取标签列表
    
    Args:
        access_token: Access Token
    
    Returns:
        list: 标签列表
    """
    url = "https://open.feishu.cn/open-apis/mail/v1/labels"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()
    
    if result.get("code") == 0:
        return result["data"]["items"]
    else:
        raise Exception(f"获取标签列表失败：{result.get('msg')}")
```

---

## 📝 实战项目：邮件管理系统

### 完整实现代码

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书邮件管理系统
Feishu Email Management System

功能:
- 发送邮件（文本/HTML）
- 查询邮件列表
- 获取邮件详情
- 删除邮件
- 管理邮件标签
- 草稿管理

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

class EmailManager:
    """邮件管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化邮件管理器
        
        Args:
            app_id: 应用 ID
            app_secret: 应用 Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis/mail/v1"
    
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
    
    # ========== 邮件发送 ==========
    
    def send_email(self, to: List[str], subject: str, content: str,
                  cc: Optional[List[str]] = None,
                  content_type: str = "text/plain") -> str:
        """
        发送邮件
        
        Args:
            to: 收件人列表
            subject: 邮件主题
            content: 邮件内容
            cc: 抄送人列表
            content_type: 内容类型
        
        Returns:
            str: 邮件 ID
        """
        url = f"{self.base_url}/messages"
        
        payload = {
            "to": to,
            "subject": subject,
            "content": content,
            "content_type": content_type
        }
        
        if cc:
            payload["cc"] = cc
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["message_id"]
        else:
            raise Exception(f"发送邮件失败：{result.get('msg')}")
    
    # ========== 邮件查询 ==========
    
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
    
    # ========== 邮件管理 ==========
    
    def delete_email(self, message_id: str) -> bool:
        """删除邮件"""
        url = f"{self.base_url}/messages/{message_id}"
        
        response = requests.delete(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    def update_labels(self, message_id: str, label_ids: List[str]) -> bool:
        """更新邮件标签"""
        url = f"{self.base_url}/messages/{message_id}/labels"
        
        payload = {"label_ids": label_ids}
        
        response = requests.put(url, headers=self._get_headers(), json=payload, timeout=10)
        result = response.json()
        
        return result.get("code") == 0
    
    # ========== 草稿管理 ==========
    
    def create_draft(self, to: List[str], subject: str, content: str,
                    cc: Optional[List[str]] = None) -> str:
        """创建草稿"""
        url = f"{self.base_url}/drafts"
        
        payload = {
            "to": to,
            "subject": subject,
            "content": content
        }
        
        if cc:
            payload["cc"] = cc
        
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
    
    # ========== 邮件夹和标签 ==========
    
    def get_folders(self) -> List[Dict]:
        """获取邮件夹列表"""
        url = f"{self.base_url}/folders"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取邮件夹列表失败：{result.get('msg')}")
    
    def get_labels(self) -> List[Dict]:
        """获取标签列表"""
        url = f"{self.base_url}/labels"
        
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["items"]
        else:
            raise Exception(f"获取标签列表失败：{result.get('msg')}")

# ========== 命令行接口 ==========

def main():
    """主函数"""
    print("=" * 60)
    print("飞书邮件管理系统 v1.0")
    print("=" * 60)
    print()
    
    # 初始化
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not all([app_id, app_secret]):
        print("❌ 请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        return
    
    manager = EmailManager(app_id, app_secret)
    
    # 菜单
    while True:
        print("\n请选择操作:")
        print("1. 发送邮件")
        print("2. 查询邮件列表")
        print("3. 获取邮件详情")
        print("4. 删除邮件")
        print("5. 创建草稿")
        print("6. 发送草稿")
        print("7. 获取邮件夹")
        print("8. 获取标签")
        print("9. 退出")
        print()
        
        choice = input("请输入选项 (1-9): ").strip()
        
        try:
            if choice == "1":
                to = input("收件人（逗号分隔）: ").strip().split(",")
                subject = input("主题：").strip()
                content = input("内容：").strip()
                content_type = input("内容类型 (text/plain 或 text/html，默认 text/plain): ").strip() or "text/plain"
                message_id = manager.send_email([x.strip() for x in to], subject, content, content_type=content_type)
                print(f"✅ 邮件发送成功：{message_id}")
            
            elif choice == "2":
                emails = manager.get_email_list()
                print(f"\n共 {len(emails)} 封邮件:")
                for email in emails[:10]:
                    print(f"  - {email.get('subject')} (from: {email.get('from')})")
            
            elif choice == "3":
                message_id = input("邮件 ID: ").strip()
                email = manager.get_email_detail(message_id)
                print(f"\n邮件详情:")
                print(f"  主题：{email.get('subject')}")
                print(f"  发件人：{email.get('from')}")
                print(f"  收件人：{email.get('to')}")
                print(f"  内容：{email.get('content')[:200]}...")
            
            elif choice == "4":
                message_id = input("邮件 ID: ").strip()
                success = manager.delete_email(message_id)
                print("✅ 删除成功" if success else "❌ 删除失败")
            
            elif choice == "5":
                to = input("收件人（逗号分隔）: ").strip().split(",")
                subject = input("主题：").strip()
                content = input("内容：").strip()
                draft_id = manager.create_draft([x.strip() for x in to], subject, content)
                print(f"✅ 草稿创建成功：{draft_id}")
            
            elif choice == "6":
                draft_id = input("草稿 ID: ").strip()
                success = manager.send_draft(draft_id)
                print("✅ 发送成功" if success else "❌ 发送失败")
            
            elif choice == "7":
                folders = manager.get_folders()
                print(f"\n共 {len(folders)} 个邮件夹:")
                for folder in folders:
                    print(f"  - {folder.get('name')} ({folder.get('folder_id')})")
            
            elif choice == "8":
                labels = manager.get_labels()
                print(f"\n共 {len(labels)} 个标签:")
                for label in labels:
                    print(f"  - {label.get('name')} ({label.get('label_id')})")
            
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
| 50001 | 邮件不存在 | 检查 message_id |
| 50002 | 收件人无效 | 检查邮箱地址格式 |
| 50003 | 草稿不存在 | 检查 draft_id |

---

## 📚 学习资源

### 官方文档

- 邮箱 API: https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 邮件发送：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN
- 草稿管理：https://open.feishu.cn/document/ukTMzTMzTMz4iMDOhEjN04SN0YjN

---

**文档版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L3-L4

📧 **邮箱 API 完整指南已创建！包含完整实现代码和实战项目！**
