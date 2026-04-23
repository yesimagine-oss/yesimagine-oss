#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 飞书邮件发送执行器
用途：解析飞书消息，调用邮件发送脚本
"""

import re
import subprocess
import sys
import json

# ==================== 消息解析 ====================

def parse_email_command(message):
    """
    解析飞书消息中的邮件命令
    
    支持的格式：
    1. 发送邮件给 xxx@example.com 主题 "xxx" 内容 "xxx"
    2. 发 Gmail 到 xxx@example.com 标题 xxx 内容 xxx
    3. send email to xxx@example.com subject xxx content xxx
    """
    
    # 模式 1: 发送邮件给 xxx 主题 "xxx" 内容 "xxx"
    pattern1 = r'发送邮件给\s*(\S+?)\s+主题\s*["\']?(.+?)["\']?\s+内容\s*["\']?(.+?)["\']?$'
    match = re.search(pattern1, message, re.IGNORECASE)
    if match:
        return {
            "to": match.group(1),
            "subject": match.group(2).strip('"\''),
            "content": match.group(3).strip('"\'')
        }
    
    # 模式 2: 发送邮件给 xxx 主题 xxx 内容 xxx（无引号）
    pattern2 = r'发送邮件给\s*(\S+?)\s+主题\s*(.+?)\s+内容\s*(.+?)$'
    match = re.search(pattern2, message, re.IGNORECASE)
    if match:
        return {
            "to": match.group(1),
            "subject": match.group(2).strip(),
            "content": match.group(3).strip()
        }
    
    # 模式 3: 发 Gmail 到 xxx 标题 xxx 内容 xxx
    pattern3 = r'发 (?:Gmail|邮件)\s*(?:到 | 给)\s*(\S+?)\s+(?:标题 | 主题)\s*(.+?)\s+内容\s*(.+?)$'
    match = re.search(pattern3, message, re.IGNORECASE)
    if match:
        return {
            "to": match.group(1),
            "subject": match.group(2).strip(),
            "content": match.group(3).strip()
        }
    
    # 模式 4: send email to xxx subject xxx content xxx
    pattern4 = r'send\s+email\s+to\s*(\S+?)\s+subject\s*(.+?)\s+(?:content|body)\s*(.+?)$'
    match = re.search(pattern4, message, re.IGNORECASE)
    if match:
        return {
            "to": match.group(1),
            "subject": match.group(2).strip(),
            "content": match.group(3).strip()
        }
    
    return None

# ==================== 发送邮件 ====================

def send_email(to_email, subject, content, use_gmail=True):
    """
    调用邮件发送脚本
    """
    
    script_path = "/home/admin/.openclaw/workspace/tools/send-email.py"
    
    cmd = [
        "python3", script_path,
        "--to", to_email,
        "--subject", subject,
        "--content", content
    ]
    
    if use_gmail:
        cmd.append("--use-gmail")
    else:
        cmd.append("--use-tencent")
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "发送超时"
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

def send_feishu_notification(status, to_email, subject, content="", error_msg=""):
    """
    发送飞书通知
    """
    
    notifier_path = "/home/admin/.openclaw/workspace/tools/feishu-email-notifier.py"
    
    cmd = [
        "python3", notifier_path,
        "--status", status,
        "--to", to_email,
        "--subject", subject
    ]
    
    if status == "success":
        cmd.extend(["--content", content])
    else:
        cmd.extend(["--error", error_msg])
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=10
        )
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"⚠️  飞书通知失败：{str(e)}")
        return False

# ==================== 主程序 ====================

def main():
    # 从命令行或标准输入获取消息
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = sys.stdin.read().strip()
    
    if not message:
        print("❌ 请提供邮件内容")
        print("\n使用示例：")
        print('  发送邮件给 xxx@example.com 主题 "测试" 内容 "你好"')
        sys.exit(1)
    
    # 解析命令
    parsed = parse_email_command(message)
    
    if not parsed:
        print("❌ 无法解析邮件命令")
        print("\n支持的格式：")
        print('  发送邮件给 xxx@example.com 主题 "测试" 内容 "你好"')
        print('  发 Gmail 到 xxx@example.com 标题 测试 内容 你好')
        sys.exit(1)
    
    print(f"📧 解析成功：")
    print(f"   收件人：{parsed['to']}")
    print(f"   主题：{parsed['subject']}")
    print(f"   内容：{parsed['content'][:50]}...")
    print()
    
    # 发送邮件
    result = send_email(
        to_email=parsed["to"],
        subject=parsed["subject"],
        content=parsed["content"]
    )
    
    # 输出结果
    if result["success"]:
        print("✅ 邮件发送成功！")
        if result["output"]:
            print(result["output"])
        
        # 发送飞书通知
        print("\n📱 发送飞书通知...")
        send_feishu_notification(
            status="success",
            to_email=parsed["to"],
            subject=parsed["subject"],
            content=parsed["content"]
        )
        
        sys.exit(0)
    else:
        print("❌ 邮件发送失败")
        if result["error"]:
            print(f"错误：{result['error']}")
        if result["output"]:
            print(f"输出：{result['output']}")
        
        # 发送飞书通知（失败）
        print("\n📱 发送飞书失败通知...")
        send_feishu_notification(
            status="failed",
            to_email=parsed["to"],
            subject=parsed["subject"],
            error_msg=result["error"] or result["output"] or "未知错误"
        )
        
        sys.exit(1)

if __name__ == "__main__":
    main()
