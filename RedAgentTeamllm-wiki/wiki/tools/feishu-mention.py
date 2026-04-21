#!/usr/bin/env python3
"""
飞书@提及功能
用于在飞书消息中正确@用户
"""

import json
import re

class FeishuMention:
    """飞书@提及工具类"""
    
    def __init__(self):
        self.mention_pattern = re.compile(r'<at[^>]*user_id=["\']([^"\']+)["\'][^>]*>([^<]+)</at>')
    
    def create_mention(self, user_id, user_name):
        """
        创建@提及字符串
        
        Args:
            user_id: 用户 ID (ou_xxxxx)
            user_name: 用户名称
        
        Returns:
            str: @提及字符串
        """
        return f'<at user_id="{user_id}">{user_name}</at>'
    
    def create_mention_all(self):
        """
        创建@所有人字符串
        
        Returns:
            str: @所有人字符串
        """
        return '<at user_id="all">所有人</at>'
    
    def parse_mention(self, text):
        """
        解析@提及
        
        Args:
            text: 包含@的文本
        
        Returns:
            list: 被@的用户列表
        """
        mentions = []
        for match in self.mention_pattern.finditer(text):
            mentions.append({
                'user_id': match.group(1),
                'user_name': match.group(2)
            })
        return mentions
    
    def format_message(self, text, mentions=None):
        """
        格式化飞书消息
        
        Args:
            text: 消息文本
            mentions: @的用户列表 [{'user_id': 'ou_xxx', 'user_name': '张三'}]
        
        Returns:
            dict: 飞书消息格式
        """
        message = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        
        if mentions:
            for mention in mentions:
                mention_str = self.create_mention(
                    mention['user_id'],
                    mention['user_name']
                )
                # 替换文本中的 @用户名 为飞书@格式
                text = text.replace(f"@{mention['user_name']}", mention_str)
            
            message['content']['text'] = text
        
        return message
    
    def create_reply_message(self, reply_to_user, content, additional_mentions=None):
        """
        创建回复消息
        
        Args:
            reply_to_user: 回复的用户 {'user_id': 'ou_xxx', 'user_name': '张三'}
            content: 回复内容
            additional_mentions: 额外@的用户列表
        
        Returns:
            dict: 飞书消息格式
        """
        mentions = [reply_to_user]
        if additional_mentions:
            mentions.extend(additional_mentions)
        
        # 构建消息文本
        text = ""
        for mention in mentions:
            text += self.create_mention(mention['user_id'], mention['user_name']) + " "
        
        text += content
        
        return self.format_message(text, mentions)
    
    def extract_user_ids(self, text):
        """
        从文本中提取用户 ID
        
        Args:
            text: 包含@的文本
        
        Returns:
            list: 用户 ID 列表
        """
        return [m['user_id'] for m in self.parse_mention(text)]
    
    def is_mentioned(self, text, user_id):
        """
        检查用户是否被@
        
        Args:
            text: 消息文本
            user_id: 用户 ID
        
        Returns:
            bool: 是否被@
        """
        return user_id in self.extract_user_ids(text)


# 命令行工具
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='飞书@提及工具')
    parser.add_argument('action', choices=['create', 'parse', 'format', 'reply'],
                       help='操作类型')
    parser.add_argument('--user-id', '-u', help='用户 ID')
    parser.add_argument('--user-name', '-n', help='用户名称')
    parser.add_argument('--text', '-t', help='消息文本')
    parser.add_argument('--content', '-c', help='回复内容')
    parser.add_argument('--all', action='store_true', help='@所有人')
    
    args = parser.parse_args()
    
    mention = FeishuMention()
    
    if args.action == 'create':
        if args.all:
            result = mention.create_mention_all()
            print(f"@所有人：{result}")
        elif args.user_id and args.user_name:
            result = mention.create_mention(args.user_id, args.user_name)
            print(f"@{args.user_name}: {result}")
        else:
            print("❌ 需要指定 --user-id 和 --user-name")
            sys.exit(1)
    
    elif args.action == 'parse':
        if not args.text:
            print("❌ 需要指定 --text")
            sys.exit(1)
        
        mentions = mention.parse_mention(args.text)
        if mentions:
            print(f"找到 {len(mentions)} 个@提及:")
            for m in mentions:
                # 隐私保护：不暴露用户 ID
                print(f"  - {m['user_name']}")
        else:
            print("未找到@提及")
    
    elif args.action == 'format':
        if not args.text:
            print("❌ 需要指定 --text")
            sys.exit(1)
        
        # 示例：格式化包含@的消息
        message = mention.format_message(args.text)
        print(json.dumps(message, indent=2, ensure_ascii=False))
    
    elif args.action == 'reply':
        if not args.user_id or not args.user_name or not args.content:
            print("❌ 需要指定 --user-id, --user-name 和 --content")
            sys.exit(1)
        
        reply_to = {'user_id': args.user_id, 'user_name': args.user_name}
        message = mention.create_reply_message(reply_to, args.content)
        print(json.dumps(message, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    import sys
    main()
