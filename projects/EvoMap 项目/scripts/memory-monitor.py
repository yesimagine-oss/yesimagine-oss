#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内存监控脚本
监控内存使用，低内存时告警
"""

import os
import logging
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
MEMORY_WARNING_MB = 100  # 可用内存<100MB 时告警
MEMORY_CRITICAL_MB = 50  # 可用内存<50MB 时严重告警
CHECK_INTERVAL = 300  # 5 分钟检查一次

# 日志配置
log_dir = Path("/home/admin/.openclaw/workspace/EvoMap 项目/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "memory-monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_memory_info():
    """获取内存信息"""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = {}
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = int(parts[1].strip().split()[0])  # KB
                    meminfo[key] = value
        
        total = meminfo.get('MemTotal', 0) / 1024  # MB
        free = meminfo.get('MemFree', 0) / 1024  # MB
        available = meminfo.get('MemAvailable', free) / 1024  # MB
        buffers = meminfo.get('Buffers', 0) / 1024  # MB
        cached = meminfo.get('Cached', 0) / 1024  # MB
        used = total - available
        
        return {
            'total_mb': total,
            'used_mb': used,
            'free_mb': free,
            'available_mb': available,
            'buffers_mb': buffers,
            'cached_mb': cached,
            'used_percent': (used / total) * 100 if total > 0 else 0,
        }
    except Exception as e:
        logger.error(f"❌ 获取内存信息失败：{e}")
        return None


def get_top_processes(n=5):
    """获取内存占用 TOP N 进程"""
    try:
        # Python 3.6 兼容
        import subprocess
        proc = subprocess.Popen(
            ['ps', 'aux', '--sort=-%mem'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = proc.communicate(timeout=10)
        
        lines = stdout.strip().split('\n')[1:n+1]  # 跳过表头
        processes = []
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    'user': parts[0],
                    'pid': parts[1],
                    'cpu': float(parts[2]),
                    'mem': float(parts[3]),
                    'command': ' '.join(parts[10:])
                })
        
        return processes
    except Exception as e:
        logger.error(f"❌ 获取进程信息失败：{e}")
        return []


def send_alert(level, message):
    """发送告警"""
    logger.warning(f"🚨 {level}: {message}")
    
    # 这里可以集成飞书通知
    # await send_feishu_alert(message)


def check_memory():
    """检查内存状态"""
    mem_info = get_memory_info()
    
    if not mem_info:
        return
    
    available = mem_info['available_mb']
    used_percent = mem_info['used_percent']
    
    logger.info(f"📊 内存使用：{mem_info['used_mb']:.0f}/{mem_info['total_mb']:.0f}MB ({used_percent:.1f}%)")
    logger.info(f"💾 可用内存：{available:.0f}MB")
    
    # 检查告警阈值
    if available < MEMORY_CRITICAL_MB:
        send_alert("🔴 严重", f"可用内存仅 {available:.0f}MB (<{MEMORY_CRITICAL_MB}MB)")
        return 'critical'
    elif available < MEMORY_WARNING_MB:
        send_alert("🟡 警告", f"可用内存 {available:.0f}MB (<{MEMORY_WARNING_MB}MB)")
        return 'warning'
    else:
        logger.info("✅ 内存充足")
        return 'normal'


def generate_report():
    """生成内存报告"""
    mem_info = get_memory_info()
    top_procs = get_top_processes()
    
    if not mem_info:
        return "❌ 无法获取内存信息"
    
    report = f"""
📊 内存监控报告

💾 总内存：{mem_info['total_mb']:.0f}MB
📈 已使用：{mem_info['used_mb']:.0f}MB ({mem_info['used_percent']:.1f}%)
💿 可用内存：{mem_info['available_mb']:.0f}MB
📦 缓存：{mem_info['cached_mb']:.0f}MB

🔝 内存占用 TOP5 进程：
"""
    
    for i, proc in enumerate(top_procs, 1):
        report += f"  {i}. {proc['command'][:50]} - {proc['mem']:.1f}%\n"
    
    return report


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("📊 内存监控检查")
    logger.info(f"⏰ 检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"⚠️  警告阈值：{MEMORY_WARNING_MB}MB")
    logger.info(f"🚨 严重阈值：{MEMORY_CRITICAL_MB}MB")
    logger.info("="*60)
    
    # 检查内存
    status = check_memory()
    
    # 生成报告
    report = generate_report()
    logger.info(report)
    
    logger.info("✅ 内存监控检查完成")


if __name__ == "__main__":
    main()
