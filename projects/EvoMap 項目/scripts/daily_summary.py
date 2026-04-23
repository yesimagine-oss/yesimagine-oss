#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 每日汇总脚本
每天 22:00 执行，发送每日汇总报告
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, '/home/admin/.openclaw/workspace/tools')


def main():
    task_name = "EvoMap 每日汇总"
    now = datetime.now()
    
    log_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'daily.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {now.strftime('%Y-%m-%d %H:%M:%S')} 每日汇总 ===\n")
    
    task_start(task_name, "生成并发送每日汇总报告", 10)
    
    # 读取当天的日志
    today_logs = []
    for log_name in ['morning.log', 'task.log', 'content.log', 'community.log']:
        log_path = os.path.join(log_dir, log_name)
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as lf:
                content = lf.read()
                if now.strftime('%Y-%m-%d') in content:
                    today_logs.append(log_name)
    
    summary = f"""
📊【EvoMap 每日汇总】

日期：{now.strftime('%Y-%m-%d')}
时间：{now.strftime('%H:%M')}

✅ 今日完成情况:
- 晨间检查：{'✅' if 'morning.log' in today_logs else '❌'}
- 任务 Claim：{'✅' if 'task.log' in today_logs else '❌'}
- 内容创作：{'✅' if 'content.log' in today_logs else '❌'}
- 社区互动：{'✅' if 'community.log' in today_logs else '❌'}

 今日总结:
- 完成任务数：待统计
- 内容产出：待统计
- 声誉变化：待统计
- 收入统计：待统计

🎯 明日计划:
- 继续每日任务循环
- 优化内容质量
- 增加社区互动

💪 今天辛苦了，明天继续！
"""
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(summary)
    
    task_end(task_name, ["每日汇总已生成", f"完成{len(today_logs)}/4 项任务"], log_file)
    
    print(summary)

if __name__ == "__main__":
    main()
