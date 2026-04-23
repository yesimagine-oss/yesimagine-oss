#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 定时任务主动监控脚本

功能:
1. 每 5 分钟检查定时任务执行状态
2. 任务未执行时自动告警
3. 自动补救执行
4. 飞书 + webUI 双渠道通知

使用:
    python3 task-monitor.py
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 日志配置
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "task-monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 定时任务配置
SCHEDULED_TASKS = {
    "07:30": {
        "name": "晨间检查",
        "script": "morning_check.py",
        "log_file": "cron_morning.log",
        "timeout_minutes": 5
    },
    "17:25": {
        "name": "任务提醒",
        "script": "task_reminder.py",
        "log_file": "cron_task.log",
        "timeout_minutes": 5
    },
    "17:30": {
        "name": "自动 Claim",
        "script": "auto-claim-task-v2.py",
        "log_file": "auto-claim.log",
        "timeout_minutes": 10
    },
    "18:10": {
        "name": "创作提醒",
        "script": "content_reminder.py",
        "log_file": "cron_content.log",
        "timeout_minutes": 5
    },
    "20:00": {
        "name": "社区互动",
        "script": "community_reminder.py",
        "log_file": "cron_community.log",
        "timeout_minutes": 5
    },
    "22:00": {
        "name": "每日汇总",
        "script": "daily_summary.py",
        "log_file": "cron_daily.log",
        "timeout_minutes": 10
    }
}

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
LOGS_DIR = PROJECT_ROOT / "logs"


def send_feishu_notification(title: str, content: str, status: str = "info"):
    """发送飞书通知"""
    emojis = {
        "success": "✅",
        "info": "📋",
        "warning": "⚠️",
        "error": "❌"
    }
    
    try:
        message = f"{emojis.get(status, '📋')} {title}\n\n{content}"
        
        result = subprocess.Popen(
            ["python3", "/home/admin/.openclaw/workspace/tools/task-notifier.py",
             "start", title, message, "5"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = result.communicate()
        
        if result.returncode == 0:
            logger.info("✅ 飞书通知发送成功")
            return True
        else:
            logger.error(f"❌ 飞书通知发送失败：{stderr}")
            return False
    
    except Exception as e:
        logger.error(f"❌ 飞书通知发送异常：{e}")
        return False


def check_task_executed(task_config: Dict, scheduled_time: datetime) -> bool:
    """
    检查任务是否已执行
    
    Args:
        task_config: 任务配置
        scheduled_time: 计划执行时间
    
    Returns:
        True if executed, False otherwise
    """
    log_file = LOGS_DIR / task_config["log_file"]
    
    if not log_file.exists():
        logger.debug(f"日志文件不存在：{log_file}")
        return False
    
    # 检查日志文件最后修改时间
    last_modified = datetime.fromtimestamp(log_file.stat().st_mtime)
    
    # 如果日志在计划时间之后更新，认为任务已执行
    if last_modified > scheduled_time - timedelta(minutes=2):
        logger.debug(f"✅ 任务已执行：{task_config['name']} (日志：{last_modified})")
        return True
    
    logger.debug(f"❌ 任务未执行：{task_config['name']} (日志：{last_modified})")
    return False


def execute_task(task_config: Dict):
    """
    执行任务脚本
    
    Args:
        task_config: 任务配置
    """
    script_path = SCRIPTS_DIR / task_config["script"]
    
    if not script_path.exists():
        logger.error(f"❌ 脚本不存在：{script_path}")
        return False
    
    try:
        logger.info(f"🚀 执行任务：{task_config['name']}")
        
        result = subprocess.Popen(
            ["python3", str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            cwd=str(PROJECT_ROOT)
        )
        stdout, stderr = result.communicate(timeout=300)
        
        if result.returncode == 0:
            logger.info(f"✅ 任务执行成功：{task_config['name']}")
            return True
        else:
            logger.error(f"❌ 任务执行失败：{task_config['name']} - {stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        logger.error(f"❌ 任务执行超时：{task_config['name']}")
        return False
    except Exception as e:
        logger.error(f"❌ 任务执行异常：{task_config['name']} - {e}")
        return False


def check_and_alert():
    """检查任务执行状态并告警"""
    logger.info("🔍 开始检查定时任务执行状态...")
    
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M")
    
    # 检查当前时间应该执行的任务
    for scheduled_time_str, task_config in SCHEDULED_TASKS.items():
        scheduled_time = datetime.strptime(
            f"{current_time.strftime('%Y-%m-%d')} {scheduled_time_str}",
            "%Y-%m-%d %H:%M"
        )
        
        # 只检查最近 10 分钟内的任务
        time_diff = current_time - scheduled_time
        if not (timedelta(minutes=0) <= time_diff <= timedelta(minutes=10)):
            continue
        
        # 检查任务是否执行
        executed = check_task_executed(task_config, scheduled_time)
        
        if not executed:
            # 任务未执行，发送告警并自动补救
            logger.warning(f"⚠️ 任务未执行：{task_config['name']} (计划：{scheduled_time_str})")
            
            # 发送告警通知
            send_feishu_notification(
                f"⚠️ 任务未执行告警",
                f"任务：{task_config['name']}\n"
                f"计划时间：{scheduled_time_str}\n"
                f"当前时间：{current_time_str}\n"
                f"延迟：{int(time_diff.total_seconds() / 60)} 分钟\n"
                f"正在自动补救执行...",
                "warning"
            )
            
            # 自动补救执行
            success = execute_task(task_config)
            
            if success:
                send_feishu_notification(
                    f"✅ 任务补救成功",
                    f"任务：{task_config['name']}\n"
                    f"计划时间：{scheduled_time_str}\n"
                    f"执行时间：{current_time_str}\n"
                    f"延迟：{int(time_diff.total_seconds() / 60)} 分钟",
                    "success"
                )
            else:
                send_feishu_notification(
                    f"❌ 任务补救失败",
                    f"任务：{task_config['name']}\n"
                    f"计划时间：{scheduled_time_str}\n"
                    f"请手动检查并执行",
                    "error"
                )
        else:
            logger.info(f"✅ 任务已执行：{task_config['name']}")
    
    logger.info("🔍 任务检查完成")


def monitor_loop():
    """主监控循环"""
    logger.info("🚀 启动定时任务监控...")
    logger.info(f"📋 监控任务数：{len(SCHEDULED_TASKS)}")
    
    import time
    
    while True:
        try:
            check_and_alert()
            time.sleep(300)  # 每 5 分钟检查一次
        except KeyboardInterrupt:
            logger.info("👋 监控停止")
            break
        except Exception as e:
            logger.error(f"❌ 监控异常：{e}")
            time.sleep(60)  # 异常后 1 分钟重试


if __name__ == "__main__":
    # 如果是命令行执行，只检查一次
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        check_and_alert()
    else:
        # 否则进入监控循环
        monitor_loop()
