#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 任务提醒脚本
每天 17:25 执行，提醒 Claim 任务
"""

import sys
import os
from datetime import datetime

# 添加工作区到路径（使用絕對路徑）
tools_path = '/home/admin/.openclaw/workspace/tools'
sys.path.insert(0, tools_path)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir('/home/admin/.openclaw/workspace')

# 导入 task_notifier
import importlib.util
spec = importlib.util.spec_from_file_location("task_notifier", os.path.join(tools_path, "task-notifier.py"))
task_notifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_notifier)
task_start = task_notifier.task_start
task_end = task_notifier.task_end

def main():
    task_name = "EvoMap 任务 Claim 提醒"
    now = datetime.now()
    
    log_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'task.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {now.strftime('%Y-%m-%d %H:%M:%S')} 任务提醒 ===\n")
    
    task_start(task_name, "提醒 Claim EvoMap 每日任务", 5)
    
    reminder = f"""
⏰【EvoMap 任务提醒】

时间：{now.strftime('%Y-%m-%d %H:%M')}

🎯 待办事项:
1️⃣ Claim 第一个任务 (17:30)
2️⃣ 执行任务内容
3️⃣ 提交任务成果

📌 提醒:
- 每天最多 Claim 3 个任务
- 任务质量影响声誉值
- 完成后记得提交审核

💪 加油！今天也要完成任务！
"""
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(reminder)
    
    task_end(task_name, ["任务提醒已发送", "Claim 时间已通知"], log_file)
    
    print(reminder)

if __name__ == "__main__":
    main()
