#!/usr/bin/env python3
"""
飞书群组成员识别 - 实际集成版本
通过 feishu_chat 工具获取群组成员
"""

import subprocess
import json
import sys

def get_chat_members(chat_id):
    """
    通过 feishu_chat 工具获取群组成员
    
    Args:
        chat_id: 群组 ID
    
    Returns:
        list: 成员列表
    """
    try:
        # 调用 feishu_chat 工具
        result = subprocess.run(
            ['openclaw', 'feishu', 'chat', '--action', 'members', '--chat-id', chat_id],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            members = data.get('members', [])
            return members
        else:
            print(f"❌ 获取成员失败：{result.stderr}")
            return []
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return []

def format_member_info(member):
    """格式化成员信息"""
    user_id = member.get('user_id', '未知')
    name = member.get('name', '未知')
    employee_id = member.get('employee_id', '')
    avatar = member.get('avatar', '')
    
    info = f"{name} ({user_id})"
    if employee_id:
        info += f" - 工号：{employee_id}"
    
    return info

def main():
    """命令行工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description='飞书群组成员获取工具')
    parser.add_argument('chat_id', help='群组 ID')
    parser.add_argument('--format', '-f', choices=['text', 'markdown', 'json'],
                       default='text', help='输出格式')
    parser.add_argument('--save', '-s', action='store_true',
                       help='保存到缓存')
    
    args = parser.parse_args()
    
    print(f"🔄 获取群组成员：{args.chat_id}\n")
    
    members = get_chat_members(args.chat_id)
    
    if not members:
        print("❌ 未获取到成员信息")
        print()
        print("可能原因:")
        print("  1. 群组 ID 错误")
        print("  2. 权限不足")
        print("  3. 网络问题")
        sys.exit(1)
    
    # 格式化输出
    if args.format == 'json':
        print(json.dumps(members, indent=2, ensure_ascii=False))
    
    elif args.format == 'markdown':
        print("### 群组成员\n")
        for i, member in enumerate(members, 1):
            name = member.get('name', '未知')
            # 隐私保护：不暴露用户 ID
            print(f"{i}. **{name}**")
    
    else:  # text
        print(f"✅ 群组 {args.chat_id} 共有 {len(members)} 个成员:\n")
        for i, member in enumerate(members, 1):
            print(f"  {i}. {format_member_info(member)}")
    
    # 保存到缓存
    if args.save:
        cache_file = '/home/admin/.openclaw/workspace/cache/feishu-group-members.json'
        try:
            import os
            from datetime import datetime
            
            os.makedirs('/home/admin/.openclaw/workspace/cache', exist_ok=True)
            
            # 加载现有缓存
            cache = {}
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
            
            # 更新缓存
            cache[args.chat_id] = {
                'timestamp': datetime.now().timestamp(),
                'expiry_seconds': 300,
                'members': members
            }
            
            # 保存缓存
            with open(cache_file, 'w') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ 已保存到缓存")
            
        except Exception as e:
            print(f"\n⚠️  保存缓存失败：{e}")

if __name__ == '__main__':
    main()
