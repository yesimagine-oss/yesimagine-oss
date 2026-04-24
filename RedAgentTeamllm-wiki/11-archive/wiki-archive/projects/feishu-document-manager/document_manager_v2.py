#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
飞书文档管理工具 - 优化版
Feishu Document Manager - Optimized Version

功能:
- 文档批量创建
- 文档内容同步
- 权限批量管理
- 文档搜索
- 文档备份

作者：OpenClaw Agent
创建时间：2026-03-13
版本：v2.0 (优化版)
"""

import os
import sys
import json
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

# 使用公共模块
from feishu_common import (
    FeishuTokenManager,
    setup_logging,
    retry,
    handle_api_errors,
    APIError,
    Config,
    DatabaseMixin,
    batch_process,
    safe_get
)

# ============================================================================
# 1. 配置
# ============================================================================

config = Config("FEISHU")

# ============================================================================
# 2. 日志配置
# ============================================================================

logger = setup_logging("document_manager")

# ============================================================================
# 3. 云文档客户端（优化版）
# ============================================================================

class DriveClient:
    """飞书云文档 API 客户端 - 优化版"""
    
    def __init__(self, token_manager: FeishuTokenManager):
        """
        初始化云文档客户端
        
        Args:
            token_manager: Token 管理器
        """
        self.token_manager = token_manager
        self.base_url = "https://open.feishu.cn"
        logger.info("云文档客户端初始化完成")
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def create_file(self, folder_token: str, title: str, 
                   file_type: str = "docx") -> Optional[str]:
        """
        创建文档
        
        Args:
            folder_token: 文件夹 Token
            title: 文档标题
            file_type: 文档类型
            
        Returns:
            Optional[str]: 文件 Token，失败返回 None
        """
        url = f"{self.base_url}/open-apis/drive/v1/files"
        payload = {
            "folder_token": folder_token,
            "title": title,
            "type": file_type
        }
        
        result = self._request("POST", url, json=payload)
        
        if result.get("code") == 0:
            file_token = result["data"]["file_token"]
            logger.info(f"文档创建成功：{title} File Token: {file_token}")
            return file_token
        else:
            logger.error(f"文档创建失败：{result.get('msg')}")
            return None
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def get_file_info(self, file_token: str) -> Optional[Dict]:
        """
        获取文档信息
        
        Args:
            file_token: 文件 Token
            
        Returns:
            Optional[Dict]: 文档信息，失败返回 None
        """
        url = f"{self.base_url}/open-apis/drive/v1/files/{file_token}"
        
        result = self._request("GET", url)
        
        if result.get("code") == 0:
            file_info = result["data"]
            logger.info(f"获取文档信息成功：{file_info.get('title')}")
            return file_info
        else:
            logger.error(f"获取文档信息失败：{result.get('msg')}")
            return None
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def batch_create_files(self, folder_token: str, titles: List[str],
                          file_type: str = "docx") -> List[str]:
        """
        批量创建文档
        
        Args:
            folder_token: 文件夹 Token
            titles: 文档标题列表
            file_type: 文档类型
            
        Returns:
            List[str]: 文件 Token 列表
        """
        logger.info(f"批量创建文档，共 {len(titles)} 个")
        
        def create_single(title: str) -> Optional[str]:
            return self.create_file(folder_token, title, file_type)
        
        # 使用批量处理工具函数
        file_tokens = batch_process(titles, batch_size=10, 
                                   process_func=create_single, delay=0.1)
        
        logger.info(f"批量创建完成，成功 {len(file_tokens)}/{len(titles)} 个")
        return file_tokens
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def search_files(self, query: str, folder_token: Optional[str] = None,
                    max_results: int = 50) -> List[Dict]:
        """
        搜索文档
        
        Args:
            query: 搜索关键词
            folder_token: 文件夹 Token
            max_results: 最大返回数量
            
        Returns:
            List[Dict]: 文档列表
        """
        url = f"{self.base_url}/open-apis/drive/v1/files/search"
        payload = {
            "query": query,
            "page_size": max_results
        }
        
        if folder_token:
            payload["folder_token"] = folder_token
        
        result = self._request("POST", url, json=payload)
        
        if result.get("code") == 0:
            files = result["data"]["items"]
            logger.info(f"搜索文档成功，共 {len(files)} 个")
            return files
        else:
            logger.error(f"搜索文档失败：{result.get('msg')}")
            return []
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def update_permission(self, file_token: str, member_id: str,
                         member_type: str = "user", 
                         role: str = "edit") -> bool:
        """
        更新文档权限
        
        Args:
            file_token: 文件 Token
            member_id: 成员 ID
            member_type: 成员类型
            role: 权限角色
            
        Returns:
            bool: 更新是否成功
        """
        url = f"{self.base_url}/open-apis/drive/v1/permissions"
        payload = {
            "file_id": file_token,
            "member": {
                "type": member_type,
                "user_id": member_id
            },
            "role": role
        }
        
        result = self._request("POST", url, json=payload)
        
        if result.get("code") == 0:
            logger.info(f"权限更新成功：{file_token} → {member_id}")
            return True
        else:
            logger.error(f"权限更新失败：{result.get('msg')}")
            return False
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def batch_update_permissions(self, file_token: str, 
                                members: List[Dict]) -> Dict[str, bool]:
        """
        批量更新文档权限
        
        Args:
            file_token: 文件 Token
            members: 成员列表 [{"user_id": "xxx", "role": "edit"}]
            
        Returns:
            Dict[str, bool]: 更新结果
        """
        logger.info(f"批量更新权限，共 {len(members)} 个成员")
        
        results = {}
        for member in members:
            member_id = safe_get(member, ["user_id"], "")
            role = safe_get(member, ["role"], "edit")
            
            success = self.update_permission(file_token, member_id, "user", role)
            results[member_id] = success
            time.sleep(0.1)
        
        return results
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def copy_file(self, file_token: str, dest_folder_token: str,
                 new_title: Optional[str] = None) -> Optional[str]:
        """
        复制文档
        
        Args:
            file_token: 文件 Token
            dest_folder_token: 目标文件夹 Token
            new_title: 新标题
            
        Returns:
            Optional[str]: 新文件 Token，失败返回 None
        """
        url = f"{self.base_url}/open-apis/drive/v1/files/{file_token}/copy"
        payload = {
            "dest_folder_token": dest_folder_token
        }
        
        if new_title:
            payload["title"] = new_title
        
        result = self._request("POST", url, json=payload)
        
        if result.get("code") == 0:
            new_file_token = result["data"]["file_token"]
            logger.info(f"文档复制成功：{new_title or '无标题'} File Token: {new_file_token}")
            return new_file_token
        else:
            logger.error(f"文档复制失败：{result.get('msg')}")
            return None
    
    @handle_api_errors
    @retry(max_retries=3, delay=1.0, backoff=2.0)
    def delete_file(self, file_token: str) -> bool:
        """
        删除文档
        
        Args:
            file_token: 文件 Token
            
        Returns:
            bool: 删除是否成功
        """
        url = f"{self.base_url}/open-apis/drive/v1/files/{file_token}"
        
        result = self._request("DELETE", url)
        
        if result.get("code") == 0:
            logger.info(f"文档删除成功：{file_token}")
            return True
        else:
            logger.error(f"文档删除失败：{result.get('msg')}")
            return False
    
    def _request(self, method: str, url: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        import requests
        headers = self.token_manager._get_headers()
        response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
        return response.json()

# ============================================================================
# 4. 文档管理工具（优化版）
# ============================================================================

class DocumentManager(DatabaseMixin):
    """文档管理工具 - 优化版主类"""
    
    def __init__(self):
        """初始化文档管理工具"""
        # 从环境变量获取配置
        app_id = config.get("APP_ID", required=True)
        app_secret = config.get("APP_SECRET", required=True)
        self.folder_token = config.get("FOLDER_TOKEN")
        
        # 初始化组件
        self.token_manager = FeishuTokenManager(app_id, app_secret)
        self.drive = DriveClient(self.token_manager)
        
        # 初始化数据库
        super().__init__("documents.db")
        
        logger.info("文档管理工具初始化完成")
    
    def _init_db(self):
        """初始化数据库表"""
        self.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_token TEXT UNIQUE,
                title TEXT,
                file_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def log_document(self, file_token: str, title: str, file_type: str):
        """记录文档信息"""
        self.execute('''
            INSERT OR REPLACE INTO documents (file_token, title, file_type)
            VALUES (?, ?, ?)
        ''', (file_token, title, file_type))
    
    def create_document(self, title: str, file_type: str = "docx") -> Optional[str]:
        """
        创建文档
        
        Args:
            title: 文档标题
            file_type: 文档类型
            
        Returns:
            Optional[str]: 文件 Token，失败返回 None
        """
        if not self.folder_token:
            logger.error("未配置 Folder Token")
            return None
        
        file_token = self.drive.create_file(self.folder_token, title, file_type)
        
        if file_token:
            self.log_document(file_token, title, file_type)
        
        return file_token
    
    def batch_create_documents(self, titles: List[str], 
                              file_type: str = "docx") -> List[str]:
        """
        批量创建文档
        
        Args:
            titles: 文档标题列表
            file_type: 文档类型
            
        Returns:
            List[str]: 文件 Token 列表
        """
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
        """
        搜索文档
        
        Args:
            query: 搜索关键词
            
        Returns:
            List[Dict]: 文档列表
        """
        return self.drive.search_files(query, self.folder_token)
    
    def share_document(self, file_token: str, user_ids: List[str],
                      role: str = "edit") -> Dict[str, bool]:
        """
        分享文档
        
        Args:
            file_token: 文件 Token
            user_ids: 用户 ID 列表
            role: 权限角色
            
        Returns:
            Dict[str, bool]: 分享结果
        """
        members = [{"user_id": uid, "role": role} for uid in user_ids]
        return self.drive.batch_update_permissions(file_token, members)
    
    def backup_documents(self, backup_folder_token: str) -> List[str]:
        """
        备份文档
        
        Args:
            backup_folder_token: 备份文件夹 Token
            
        Returns:
            List[str]: 备份文件 Token 列表
        """
        logger.info("开始备份文档")
        
        # 查询所有文档
        documents = self.execute("SELECT file_token, title FROM documents")
        
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
        documents = self.execute("SELECT file_token, title, file_type, created_at FROM documents")
        
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
        # 总文档数
        total = self.execute("SELECT COUNT(*) FROM documents")[0][0]
        
        # 按类型统计
        by_type_result = self.execute("SELECT file_type, COUNT(*) FROM documents GROUP BY file_type")
        by_type = dict(by_type_result)
        
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
    print("飞书文档管理工具 v2.0 (优化版)")
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
