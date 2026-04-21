#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 定时任务状态检查脚本

用途：检查定时任务配置和执行情况
"""

import subprocess
import os
from datetime import datetime

def check_crontab():
    """检查 crontab 配置"""
    print("📋 检查 Crontab 配置")
    print("=" * 60)
    
    result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        evomap_tasks = [line for line in lines if 'EvoMap' in line or 'scripts/' in line]
        
        if evomap_tasks:
            print(f"✅ 找到 {len(evomap_tasks)} 个 EvoMap 定时任务:\n")
            for task in evomap_tasks:
                if not task.startswith('#'):
                    print(f"  {task}")
                else:
                    print(f"  {task}")
        else:
            print("❌ 未找到 EvoMap 定时任务")
    else:
        print("❌ 无法读取 crontab")
    
    print()

def check_scripts():
    """检查脚本文件"""
    print("📁 检查脚本文件")
    print("=" * 60)
    
    scripts_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/scripts'
    expected_scripts = [
        'morning_check.py',
        'task_reminder.py',
        'content_reminder.py',
        'community_reminder.py',
        'daily_summary.py'
    ]
    
    if not os.path.exists(scripts_dir):
        print(f"❌ 脚本目录不存在：{scripts_dir}")
        return
    
    for script in expected_scripts:
        script_path = os.path.join(scripts_dir, script)
        if os.path.exists(script_path):
            size = os.path.getsize(script_path)
            executable = os.access(script_path, os.X_OK)
            status = "✅" if executable else "⚠️ "
            print(f"  {status} {script} ({size} bytes, {'可执行' if executable else '不可执行'})")
        else:
            print(f"  ❌ {script} (不存在)")
    
    print()

def check_logs():
    """检查日志文件"""
    print("📊 检查日志文件")
    print("=" * 60)
    
    logs_dir = '/home/admin/.openclaw/workspace/EvoMap 項目/logs'
    
    if not os.path.exists(logs_dir):
        print(f"❌ 日志目录不存在：{logs_dir}")
        return
    
    log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
    
    if log_files:
        print(f"找到 {len(log_files)} 个日志文件:\n")
        for log_file in sorted(log_files):
            log_path = os.path.join(logs_dir, log_file)
            size = os.path.getsize(log_path)
            mtime = datetime.fromtimestamp(os.path.getmtime(log_path))
            print(f"  📄 {log_file} ({size} bytes, 最后更新：{mtime.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("  📭 暂无日志文件（正常，等待首次执行）")
    
    print()

def check_next_run():
    """计算下次执行时间"""
    print("⏰ 下次执行时间")
    print("=" * 60)
    
    now = datetime.now()
    
    schedules = [
        ("晨间检查", 7, 30),
        ("任务提醒", 17, 25),
        ("创作提醒", 18, 10),
        ("社区提醒", 20, 0),
        ("每日汇总", 22, 0)
    ]
    
    for task_name, hour, minute in schedules:
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if now >= next_run:
            # 今天的已经过了，算明天
            from datetime import timedelta
            next_run += timedelta(days=1)
        
        delta = next_run - now
        hours_remaining = int(delta.total_seconds() // 3600)
        minutes_remaining = int((delta.total_seconds() % 3600) // 60)
        
        print(f"  {task_name}: {next_run.strftime('%Y-%m-%d %H:%M')} ({hours_remaining}小时{minutes_remaining}分钟后)")
    
    print()

def main():
    print("\n🔍 EvoMap 定时任务状态检查")
    print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    check_crontab()
    check_scripts()
    check_logs()
    check_next_run()
    
    print("=" * 60)
    print("✅ 检查完成！")
    print()

if __name__ == "__main__":
    main()
