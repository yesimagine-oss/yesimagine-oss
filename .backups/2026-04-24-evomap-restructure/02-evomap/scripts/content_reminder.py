#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 内容创作提醒脚本
每天 18:10 执行，提醒开始内容创作
"""

import sys
import os
from datetime import datetime

# 添加工作区到路径
tools_path = '/home/admin/.openclaw/workspace/tools'
sys.path.insert(0, tools_path)
os.chdir(tools_path)

# 导入 task_notifier
import importlib.util
spec = importlib.util.spec_from_file_location("task_notifier", os.path.join(tools_path, "task-notifier.py"))
task_notifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_notifier)
task_start = task_notifier.task_start
task_end = task_notifier.task_end


def main():
    task_name = "EvoMap 内容创作提醒"
    now = datetime.now()
    
    log_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'content.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {now.strftime('%Y-%m-%d %H:%M:%S')} 创作提醒 ===\n")
    
    task_start(task_name, "提醒开始第一篇内容创作", 45)
    
    reminder = f"""
✍️【EvoMap 内容创作提醒】

时间：{now.strftime('%Y-%m-%d %H:%M')}

📝 创作任务:
1️⃣ 18:15 开始第一篇内容创作
2️⃣ 19:45 完成内容创作
3️⃣ 预留 90 分钟创作时间

💡 创作建议:
- 结合今日任务经验
- 分享实操心得
- 保持真实有价值
- 注意内容质量

🎯 目标:
- 每日至少 1 篇优质内容
- 积累粉丝和影响力
- 为知识变现打基础

🚀 开始创作吧！
"""
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(reminder)
    
    task_end(task_name, ["创作提醒已发送", "创作时间已安排"], log_file)
    
    print(reminder)

if __name__ == "__main__":
    main()
