#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 社区互动提醒脚本
每天 20:00 执行，提醒社区互动
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, '/home/admin/.openclaw/workspace/tools')


def main():
    task_name = "EvoMap 社区互动提醒"
    now = datetime.now()
    
    log_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'community.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {now.strftime('%Y-%m-%d %H:%M:%S')} 社区提醒 ===\n")
    
    task_start(task_name, "提醒进行社区互动", 60)
    
    reminder = f"""
🤝【EvoMap 社区互动提醒】

时间：{now.strftime('%Y-%m-%d %H:%M')}

💬 互动任务:
1️⃣ 20:00 开始社区互动
2️⃣ 20:00-21:00 互动时间
3️⃣ 回复评论和私信
4️⃣ 参与话题讨论

📌 互动建议:
- 真诚回复每一条评论
- 主动参与热门话题
- 建立粉丝关系
- 收集用户反馈

🎯 目标:
- 提高账号活跃度
- 增加粉丝粘性
- 扩大影响力

💪 社区是成长的关键！
"""
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(reminder)
    
    task_end(task_name, ["社区互动提醒已发送", "互动时间已安排"], log_file)
    
    print(reminder)

if __name__ == "__main__":
    main()
