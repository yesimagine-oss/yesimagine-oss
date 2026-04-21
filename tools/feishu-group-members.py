#!/usr/bin/env python3
"""
飞书群组成员识别工具
用于获取、缓存和显示群组成员信息
"""

import json
import os
import sys
from datetime import datetime, timedelta

# 缓存文件位置
CACHE_DIR = '/home/admin/.openclaw/workspace/cache'
MEMBERS_CACHE_FILE = os.path.join(CACHE_DIR, 'feishu-group-members.json')
CACHE_EXPIRY_SECONDS = 300  # 5 分钟缓存

class GroupMemberManager:
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.cache_file = MEMBERS_CACHE_FILE
        self.members_cache = {}
        self.load_cache()
    
    def load_cache(self):
        """加载缓存"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.members_cache = json.load(f)
                print(f"✅ 已加载缓存 ({len(self.members_cache)} 个群组)")
            else:
                print("ℹ️  缓存不存在，将创建新缓存")
        except Exception as e:
            print(f"⚠️  加载缓存失败：{e}")
            self.members_cache = {}
    
    def save_cache(self):
        """保存缓存"""
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.members_cache, f, indent=2, ensure_ascii=False)
            print(f"✅ 缓存已保存 ({len(self.members_cache)} 个群组)")
        except Exception as e:
            print(f"❌ 保存缓存失败：{e}")
    
    def is_cache_valid(self, chat_id):
        """检查缓存是否有效"""
        if chat_id not in self.members_cache:
            return False
        
        cache_time = self.members_cache[chat_id].get('timestamp', 0)
        cache_expiry = self.members_cache[chat_id].get('expiry_seconds', CACHE_EXPIRY_SECONDS)
        
        # 检查是否过期
        if datetime.now().timestamp() - cache_time > cache_expiry:
            print(f"ℹ️  群组 {chat_id} 缓存已过期")
            return False
        
        return True
    
    def get_members(self, chat_id):
        """
        获取群组成员
        
        Args:
            chat_id: 群组 ID
        
        Returns:
            list: 成员列表
        """
        # 检查缓存
        if self.is_cache_valid(chat_id):
            print(f"✅ 使用缓存：群组 {chat_id}")
            return self.members_cache[chat_id]['members']
        
        # 缓存无效，需要刷新
        print(f"🔄 刷新群组成员：{chat_id}")
        return self.refresh_members(chat_id)
    
    def refresh_members(self, chat_id):
        """
        刷新群组成员
        
        实际使用时需要调用 feishu_chat 工具
        这里提供接口和缓存逻辑
        """
        print("⚠️  需要通过 feishu_chat 工具获取成员")
        print()
        print("使用方法:")
        print("  feishu_chat(action='members', chat_id='群组 ID')")
        print()
        
        # 这里应该调用 feishu_chat API
        # 由于当前环境限制，返回示例数据
        return []
    
    def format_members(self, members, format='text'):
        """
        格式化成员列表
        
        Args:
            members: 成员列表
            format: 输出格式 (text/markdown/json)
        
        Returns:
            str: 格式化后的成员列表
        """
        if not members:
            return "暂无成员信息"
        
        if format == 'json':
            return json.dumps(members, indent=2, ensure_ascii=False)
        
        elif format == 'markdown':
            lines = ["### 群组成员\n"]
            for i, member in enumerate(members, 1):
                name = member.get('name', '未知')
                user_id = member.get('user_id', '未知')
                lines.append(f"{i}. **{name}** (`{user_id}`)")
            return '\n'.join(lines)
        
        else:  # text
            lines = ["群组成员:"]
            for i, member in enumerate(members, 1):
                name = member.get('name', '未知')
                user_id = member.get('user_id', '未知')
                lines.append(f"  {i}. {name} ({user_id})")
            return '\n'.join(lines)
    
    def find_member_by_name(self, chat_id, name):
        """
        根据名称查找成员
        
        Args:
            chat_id: 群组 ID
            name: 成员名称（可以是部分匹配）
        
        Returns:
            dict: 成员信息，未找到返回 None
        """
        members = self.get_members(chat_id)
        
        # 精确匹配
        for member in members:
            if member.get('name') == name:
                return member
        
        # 模糊匹配
        for member in members:
            if name in member.get('name', ''):
                return member
        
        return None
    
    def find_member_by_id(self, chat_id, user_id):
        """
        根据 ID 查找成员
        
        Args:
            chat_id: 群组 ID
            user_id: 用户 ID
        
        Returns:
            dict: 成员信息，未找到返回 None
        """
        members = self.get_members(chat_id)
        
        for member in members:
            if member.get('user_id') == user_id:
                return member
        
        return None
    
    def clear_cache(self):
        """清除缓存"""
        self.members_cache = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        print("✅ 缓存已清除")
    
    def list_cached_groups(self):
        """列出缓存的群组"""
        if not self.members_cache:
            print("ℹ️  缓存为空")
            return
        
        print("缓存的群组:")
        for chat_id, data in self.members_cache.items():
            timestamp = datetime.fromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            member_count = len(data['members'])
            print(f"  - {chat_id}: {member_count} 个成员 (更新于 {timestamp})")


def main():
    """命令行工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description='飞书群组成员管理工具')
    parser.add_argument('action', choices=['list', 'refresh', 'clear', 'find', 'show'],
                       help='操作类型')
    parser.add_argument('--chat-id', '-c', help='群组 ID')
    parser.add_argument('--name', '-n', help='查找的成员名称')
    parser.add_argument('--format', '-f', choices=['text', 'markdown', 'json'],
                       default='text', help='输出格式')
    
    args = parser.parse_args()
    
    manager = GroupMemberManager()
    
    if args.action == 'list':
        manager.list_cached_groups()
    
    elif args.action == 'clear':
        manager.clear_cache()
    
    elif args.action == 'refresh':
        if not args.chat_id:
            print("❌ 需要指定 --chat-id")
            sys.exit(1)
        members = manager.refresh_members(args.chat_id)
        print(manager.format_members(members, args.format))
        manager.save_cache()
    
    elif args.action == 'find':
        if not args.chat_id or not args.name:
            print("❌ 需要指定 --chat-id 和 --name")
            sys.exit(1)
        member = manager.find_member_by_name(args.chat_id, args.name)
        if member:
            print("找到成员:")
            print(json.dumps(member, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 未找到成员：{args.name}")
    
    elif args.action == 'show':
        if not args.chat_id:
            print("❌ 需要指定 --chat-id")
            sys.exit(1)
        members = manager.get_members(args.chat_id)
        print(manager.format_members(members, args.format))


if __name__ == '__main__':
    main()
