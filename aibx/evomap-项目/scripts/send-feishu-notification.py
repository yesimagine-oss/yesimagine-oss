#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过 OpenClaw message 工具发送飞书通知
"""

import subprocess
import sys
import json

def send_feishu_message(chat_id, message):
    """使用 OpenClaw message 工具发送飞书消息"""
    
    cmd = [
        "openclaw", "message", "send",
        "--target", chat_id,
        "--message", message
    ]
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
        if result.returncode == 0:
            print("✅ 飞书消息已发送")
            return True
        else:
            print("❌ 发送失败：" + result.stderr[:200])
            return False
    except Exception as e:
        print("❌ 异常：" + str(e))
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python3 send-feishu-notification.py <chat_id> <message>")
        sys.exit(1)
    
    chat_id = sys.argv[1]
    message = sys.argv[2]
    
    success = send_feishu_message(chat_id, message)
    sys.exit(0 if success else 1)
