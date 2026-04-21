#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书文档管理工具
Feishu Document Manager

功能:
- 文档批量创建
- 文档内容同步
- 权限批量管理
- 文档搜索
- 文档备份

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v1.0
"""

import os
import sys
import json
import time
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============================================================================
# 1. 日志配置
# ============================================================================

def setup_logging():
    """配置日志"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"document_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# 2. Token 管理器
# ============================================================================

class FeishuTokenManager:
    """飞书 Token 管理器"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_access_token: Optional[str] = None
        self.token_expire_time: float = 0
        logger.info("Token 管理器初始化完成")
    
    def get_app_access_token(self) -> str:
        """获取应用 Access Token"""
        if self.app_access_token and time.time() < self.token_expire_time:
            return self.app_access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if result.get("code") != 0:
                raise Exception(f"获取 Token 失败：{result.get('msg')}")
            
            self.app_access_token = result["app_access_token"]
            self.token_expire_time = time.time() + 7200 - 600
            
            logger.info(f"获取新 Token 成功")
            return self.app_access_token
        
        except Exception as e:
            logger.error(f"获取 Token 失败：{e}")
            raise
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.get_app_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

# ============================================================================
# 3. 云文档 API 客户端
# ============================================================================

class DriveClient:
    """飞书云文档 API 客户端"""
    
    def __init__(self, token_manager: FeishuTokenManager):
        self.token_manager = token_manager
        self.base_url = "https://open.feishu.cn"
        logger.info("云文档客户端初始化完成")
    
    def create_file(self, folder_token: str, title: str, 
                   file_type: str = "docx") -> Optional[str]:
        """创建文档"""
        url = f"{self.base_url}/open-apis/drive/v1/files"
        payload = {
            "folder_token": folder_token,
            "title": title,
            "type": file_type
        }
        
        try:
            response = requests.post(
                url,
                headers=self.token_manager._get_headers(),
                json=payload,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                file_token = result["data"]["file_token"]
                logger.info(f"文档创建成功：{title} File Token: {file_token}")
                return file_token
            else:
                logger.error(f"文档创建失败：{result.get('msg')}")
                return None
        
        except Exception as e:
            logger.error(f"文档创建异常：{e}")
            return None
    
    def get_file_info(self, file_token: str) -> Optional[Dict]:
        """获取文档信息"""
        url = f"{self.base_url}/open-apis/drive/v1/files/{file_token}"
        
        try:
            response = requests.get(
                url,
                headers=self.token_manager._get_headers(),
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                file_info = result["data"]
                logger.info(f"获取文档信息成功：{file_info.get('title')}")
                return file_info
            else:
                logger.error(f"获取文档信息失败：{result.get('msg')}")
                return None
        
        except Exception as e:
            logger.error(f"获取文档信息异常：{e}")
            return None
    
    def batch_create_files(self, folder_token: str, titles: List[str],
                          file_type: str = "docx") -> List[str]:
        """批量创建文档"""
        logger.info(f"批量创建文档，共 {len(titles)} 个")
        
        file_tokens = []
        for i, title in enumerate(titles, 1):
            logger.info(f"创建第 {i}/{len(titles)} 个文档：{title}")
            file_token = self.create_file(folder_token, title, file_type)
            if file_token:
                file_tokens.append(file_token)
            time.sleep(0.1)  # 避免频率限制
        
        logger.info(f"批量创建完成，成功 {len(file_tokens)}/{len(titles)} 个")
        return file_tokens
    
    def search_files(self, query: str, folder_token: Optional[str] = None,
                    max_results: int = 50) -> List[Dict]:
        """搜索文档"""
        url = f"{self.base_url}/open-apis/drive/v1/files/search"
        payload = {
            "query": query,
            "page_size": max_results
        }
        
        if folder_token:
            payload["folder_token"] = folder_token
        
        try:
            response = requests.post(
                url,
                headers=self.token_manager._get_headers(),
                json=payload,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                files = result["data"]["items"]
                logger.info(f"搜索文档成功，共 {len(files)} 个")
                return files
            else:
                logger.error(f"搜索文档失败：{result.get('msg')}")
                return []
        
        except Exception as e:
            logger.error(f"搜索文档异常：{e}")
            return []
    
    def update_permission(self, file_token: str, member_id: str,
                         member_type: str = "user", 
                         role: str = "edit") -> bool:
        """更新文档权限"""
        url = f"{self.base_url}/open-apis/drive/v1/permissions"
        payload = {
            "file_id": file_token,
            "member": {
                "type": member_type,
                "user_id": member_id
            },
            "role": role
        }
        
        try:
            response = requests.post(
                url,
                headers=self.token_manager._get_headers(),
                json=payload,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                logger.info(f"权限更新成功：{file_token} → {member_id}")
                return True
            else:
                logger.error(f"权限更新失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            logger.error(f"权限更新异常：{e}")
            return False
    
    def batch_update_permissions(self, file_token: str, 
                                members: List[Dict]) -> Dict[str, bool]:
        """批量更新文档权限"""
        logger.info(f"批量更新权限，共 {len(members)} 个成员")
        
        results = {}
        for i, member in enumerate(members, 1):
            member_id = member.get("user_id")
            role = member.get("role", "edit")
            logger.info(f"更新第 {i}/{len(members)} 个权限：{member_id} → {role}")
            
            success = self.update_permission(file_token, member_id, "user", role)
            results[member_id] = success
            time.sleep(0.1)
        
        return results
    
    def copy_file(self, file_token: str, dest_folder_token: str,
                 new_title: Optional[str] = None) -> Optional[str]:
        """复制文档"""
        url = f"{self.base_url}/open-apis/drive/v1/files/{file_token}/copy"
        payload = {
            "dest_folder_token": dest_folder_token
        }
        
        if new_title:
            payload["title"] = new_title
        
        try:
            response = requests.post(
                url,
                headers=self.token_manager._get_headers(),
                json=payload,
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                new_file_token = result["data"]["file_token"]
                logger.info(f"文档复制成功：{new_title or '无标题'} File Token: {new_file_token}")
                return new_file_token
            else:
                logger.error(f"文档复制失败：{result.get('msg')}")
                return None
        
        except Exception as e:
            logger.error(f"文档复制异常：{e}")
            return None
    
    def delete_file(self, file_token: str) -> bool:
        """删除文档"""
        url = f"{self.base_url}/open-apis/drive/v1/files/{file_token}"
        
        try:
            response = requests.delete(
                url,
                headers=self.token_manager._get_headers(),
                timeout=10
            )
            result = response.json()
            
            if result.get("code") == 0:
                logger.info(f"文档删除成功：{file_token}")
                return True
            else:
                logger.error(f"文档删除失败：{result.get('msg')}")
                return False
        
        except Exception as e:
            logger.error(f"文档删除异常：{e}")
            return False

# ============================================================================
# 4. 文档管理工具主类
# ============================================================================

class DocumentManager:
    """文档管理工具主类"""
    
    def __init__(self):
        # 从环境变量获取配置
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.app_secret = os.getenv("FEISHU_APP_SECRET")
        self.folder_token = os.getenv("FEISHU_FOLDER_TOKEN")
        
        if not all([self.app_id, self.app_secret]):
            raise Exception("请设置环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET")
        
        # 初始化组件
        self.token_manager = FeishuTokenManager(self.app_id, self.app_secret)
        self.drive = DriveClient(self.token_manager)
        
        # 初始化数据库
        self.db_path = "documents.db"
        self.init_database()
        
        logger.info("文档管理工具初始化完成")
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_token TEXT UNIQUE,
                title TEXT,
                file_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logger.info(f"数据库初始化完成：{self.db_path}")
    
    def log_document(self, file_token: str, title: str, file_type: str):
        """记录文档信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO documents (file_token, title, file_type)
            VALUES (?, ?, ?)
        ''', (file_token, title, file_type))
        conn.commit()
        conn.close()
    
    def create_document(self, title: str, file_type: str = "docx") -> Optional[str]:
        """创建文档"""
        if not self.folder_token:
            logger.error("未配置 Folder Token")
            return None
        
        file_token = self.drive.create_file(self.folder_token, title, file_type)
        
        if file_token:
            self.log_document(file_token, title, file_type)
        
        return file_token
    
    def batch_create_documents(self, titles: List[str], 
                              file_type: str = "docx") -> List[str]:
        """批量创建文档"""
        if not self.folder_token:
            logger.error("未配置 Folder Token")
            return []
        
        file_tokens = self.drive.batch_create_files(self.folder_token, titles, file_type)
        
        for token in file_tokens:
            file_info = self.drive.get_file_info(token)
            if file_info:
                self.log_document(token, file_info.get("title", ""), file_type)
        
        return file_tokens
    
    def search_documents(self, query: str) -> List[Dict]:
        """搜索文档"""
        return self.drive.search_files(query, self.folder_token)
    
    def share_document(self, file_token: str, user_ids: List[str],
                      role: str = "edit") -> Dict[str, bool]:
        """分享文档"""
        members = [{"user_id": uid, "role": role} for uid in user_ids]
        return self.drive.batch_update_permissions(file_token, members)
    
    def backup_documents(self, backup_folder_token: str) -> List[str]:
        """备份文档"""
        logger.info("开始备份文档")
        
        # 查询所有文档
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT file_token, title FROM documents")
        documents = cursor.fetchall()
        conn.close()
        
        backup_tokens = []
        for file_token, title in documents:
            logger.info(f"备份文档：{title}")
            new_title = f"{title}_backup_{datetime.now().strftime('%Y%m%d')}"
            new_token = self.drive.copy_file(file_token, backup_folder_token, new_title)
            if new_token:
                backup_tokens.append(new_token)
            time.sleep(0.1)
        
        logger.info(f"备份完成，共 {len(backup_tokens)} 个文档")
        return backup_tokens
    
    def list_documents(self):
        """列出所有文档"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT file_token, title, file_type, created_at FROM documents")
        documents = cursor.fetchall()
        conn.close()
        
        print("\n" + "=" * 80)
        print("文档列表")
        print("=" * 80)
        
        if not documents:
            print("暂无文档")
            return
        
        for i, doc in enumerate(documents, 1):
            print(f"\n{i}. {doc[1]}")
            print(f"   Token: {doc[0]}")
            print(f"   类型：{doc[2]}")
            print(f"   创建时间：{doc[3]}")
        
        print("=" * 80)
        print(f"共 {len(documents)} 个文档")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总文档数
        cursor.execute("SELECT COUNT(*) FROM documents")
        total = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute("SELECT file_type, COUNT(*) FROM documents GROUP BY file_type")
        by_type = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            "total": total,
            "by_type": by_type
        }
    
    def close(self):
        """关闭文档管理工具"""
        logger.info("文档管理工具已关闭")

# ============================================================================
# 5. 命令行接口
# ============================================================================

def main():
    """主函数"""
    print("=" * 80)
    print("飞书文档管理工具 v1.0")
    print("=" * 80)
    print()
    print("请选择操作:")
    print("1. 创建文档")
    print("2. 批量创建文档")
    print("3. 搜索文档")
    print("4. 分享文档")
    print("5. 备份文档")
    print("6. 列出所有文档")
    print("7. 查看统计信息")
    print("8. 退出")
    print()
    
    try:
        manager = DocumentManager()
        
        while True:
            choice = input("请输入选项 (1-8): ").strip()
            
            if choice == "1":
                title = input("文档标题：").strip()
                file_type = input("文档类型 (docx/sheet/file): ").strip() or "docx"
                file_token = manager.create_document(title, file_type)
                
                if file_token:
                    print(f"✅ 文档创建成功：{file_token}")
                else:
                    print("❌ 文档创建失败")
            
            elif choice == "2":
                print("输入文档标题（每行一个，空行结束）:")
                titles = []
                while True:
                    title = input().strip()
                    if not title:
                        break
                    titles.append(title)
                
                file_type = input("文档类型 (docx/sheet/file): ").strip() or "docx"
                file_tokens = manager.batch_create_documents(titles, file_type)
                
                print(f"✅ 批量创建完成，成功 {len(file_tokens)}/{len(titles)} 个")
            
            elif choice == "3":
                query = input("搜索关键词：").strip()
                documents = manager.search_documents(query)
                
                print(f"\n找到 {len(documents)} 个文档:")
                for i, doc in enumerate(documents, 1):
                    print(f"{i}. {doc.get('title', '无标题')} ({doc.get('type', '未知类型')})")
            
            elif choice == "4":
                file_token = input("文档 Token: ").strip()
                user_ids = input("用户 ID 列表（逗号分隔）: ").strip().split(",")
                role = input("权限角色 (edit/view/comment): ").strip() or "edit"
                
                results = manager.share_document(file_token, user_ids, role)
                
                success_count = sum(1 for v in results.values() if v)
                print(f"✅ 分享完成，成功 {success_count}/{len(user_ids)} 个")
            
            elif choice == "5":
                backup_folder = input("备份文件夹 Token: ").strip()
                backup_tokens = manager.backup_documents(backup_folder)
                print(f"✅ 备份完成，共 {len(backup_tokens)} 个文档")
            
            elif choice == "6":
                manager.list_documents()
            
            elif choice == "7":
                stats = manager.get_stats()
                print("\n统计信息:")
                print(f"  总文档数：{stats['total']}")
                print("  按类型统计:")
                for file_type, count in stats['by_type'].items():
                    print(f"    {file_type}: {count}")
            
            elif choice == "8":
                manager.close()
                print("再见！")
                break
            
            else:
                print("无效选项，请重新输入")
    
    except Exception as e:
        logger.error(f"程序异常：{e}")
        print(f"错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
