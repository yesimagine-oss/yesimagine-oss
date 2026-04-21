#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bundle 发布冷却结束提醒
冷却时间：08:45
"""

import time
from datetime import datetime
from pathlib import Path
import subprocess

LOG_FILE = Path(__file__).parent / "logs" / "bundle_cooldown.log"
LOG_FILE.parent.mkdir(exist_ok=True)

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def send_feishu(content: str):
    """发送飞书消息"""
    try:
        cmd = [
            'openclaw', 'message', 'send',
            '--target', 'ou_f4919832188bcc630f8f257497fa93a4',
            '--channel', 'feishu',
            '--message', content
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            log("✅ 飞书推送成功")
        else:
            log(f"❌ 飞书推送失败：{result.stderr}")
    except Exception as e:
        log(f"❌ 飞书推送异常：{e}")

def main():
    log("="*60)
    log("🔔 Bundle 发布冷却提醒启动")
    log("="*60)
    log("冷却结束时间：08:45")
    log("待发布 Bundle:")
    log("  • #2: 数据库连接池优化")
    log("  • #3: WebSocket 断线重连")
    log("")
    log("🚀 提醒运行中...")
    log("")
    
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        if current_time == "08:45":
            log("⏰ 冷却结束！")
            send_feishu("""🔔 发布冷却已结束

Bundle #2: 数据库连接池优化
Bundle #3: WebSocket 断线重连

可以重新发布了！""")
            break
        
        time.sleep(30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("")
        log("👋 提醒已停止")
