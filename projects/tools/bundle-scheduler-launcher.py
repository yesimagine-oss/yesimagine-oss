#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bundle 制作任务启动器
功能：检查并启动 bundle_plan_scheduler_final.py 后台运行
执行时间：每日 22:15
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# 配置
SCRIPT_DIR = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目")
SCHEDULER_SCRIPT = SCRIPT_DIR / "bundle_plan_scheduler_final.py"
LOG_DIR = SCRIPT_DIR / "logs"
PID_FILE = LOG_DIR / "bundle_scheduler.pid"
LOG_FILE = Path(__file__).parent.parent / "logs" / "bundle-launcher.log"

# 确保日志目录存在
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log(message: str):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def is_running() -> bool:
    """检查调度器是否已在运行"""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # 检查进程是否存在
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError):
        # 进程不存在或 PID 文件无效
        if PID_FILE.exists():
            PID_FILE.unlink()
        return False

def start_scheduler():
    """启动调度器后台运行"""
    log("🚀 启动 Bundle 制作调度器...")
    
    # 使用 nohup 后台运行
    nohup_cmd = [
        'nohup',
        'python3',
        str(SCHEDULER_SCRIPT),
        '>', str(LOG_DIR / 'bundle_plan_nohup.log'),
        '2>&1',
        '&'
    ]
    
    # 直接使用 subprocess 启动
    proc = subprocess.Popen(
        ['python3', str(SCHEDULER_SCRIPT)],
        stdout=open(LOG_DIR / 'bundle_plan_nohup.log', 'a'),
        stderr=subprocess.STDOUT,
        start_new_session=True,
        cwd=str(SCRIPT_DIR)
    )
    
    # 保存 PID
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    log(f"✅ 调度器已启动 (PID: {proc.pid})")
    log(f"📁 日志文件：{LOG_DIR / 'bundle_plan.log'}")
    log(f"⏰ 执行时间：22:15 - 05:20")
    
    return True

def stop_scheduler():
    """停止调度器"""
    if not PID_FILE.exists():
        log("⚠️  PID 文件不存在，调度器可能未运行")
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        os.kill(pid, 0)  # 检查进程是否存在
        os.kill(pid, 15)  # 发送 SIGTERM
        
        log(f"✅ 调度器已停止 (PID: {pid})")
        
        if PID_FILE.exists():
            PID_FILE.unlink()
        
        return True
    except (ProcessLookupError, ValueError):
        log("⚠️  进程不存在，清理 PID 文件")
        if PID_FILE.exists():
            PID_FILE.unlink()
        return False

def main():
    """主函数"""
    log("=" * 60)
    log("📦 Bundle 制作任务启动器")
    log("=" * 60)
    
    # 检查脚本是否存在
    if not SCHEDULER_SCRIPT.exists():
        log(f"❌ 调度器脚本不存在：{SCHEDULER_SCRIPT}")
        sys.exit(1)
    
    # 检查是否已在运行
    if is_running():
        log("✅ 调度器已在运行，无需重复启动")
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        log(f"   PID: {pid}")
    else:
        log("⚠️  调度器未运行，启动...")
        start_scheduler()
    
    log("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("⚠️  用户中断")
    except Exception as e:
        log(f"❌ 执行异常：{e}")
        import traceback
        log(traceback.format_exc())
