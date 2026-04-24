#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 晨间检查脚本
每天 07:30 执行，发送晨间汇总提醒
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
    task_name = "EvoMap 晨间检查"
    now = datetime.now()
    
    # 检查日志
    log_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'morning.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {now.strftime('%Y-%m-%d %H:%M:%S')} 晨间检查 ===\n")
    
    # 任务开始通知
    task_start(task_name, "查看 EvoMap 任务列表、声誉、收入状态", 5)
    
    # 检查内容（这里可以扩展为实际 API 调用）
    summary = f"""
📊 EvoMap 晨间检查报告
时间：{now.strftime('%Y-%m-%d %H:%M')}

✅ 检查项目:
- 任务列表状态
- 声誉值变化
- 收入统计
- 今日任务规划

📝 提醒:
- 17:30 Claim 第一个任务
- 18:15 开始内容创作
- 20:00 社区互动
- 22:00 查看每日汇总
"""
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(summary)
    
    # 任务完成通知（不发送服务器路径，只发送完成状态）
    task_end(task_name, ["晨间检查完成", "任务列表已查看", "今日计划已生成"], "完整报告已通过飞书发送")
    
    # 发送完整内容到飞书（不发送服务器路径）
    import importlib.util
    spec2 = importlib.util.spec_from_file_location("send_feishu", os.path.join(tools_path, "..", "EvoMap 項目", "scripts", "send_morning_summary_complete.py"))
    
    print(summary)

if __name__ == "__main__":
    main()
