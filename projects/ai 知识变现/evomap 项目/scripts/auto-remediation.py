#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
失败自动补救脚本

功能:
1. 检测任务失败
2. 自动执行补救措施
3. 发送补救通知
4. 记录补救历史
"""

import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# 日志配置
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "auto-remediation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 补救配置
REMEDIATION_CONFIG = {
    "morning_check": {
        "max_retries": 3,
        "retry_interval_minutes": 5,
        "script": "morning_check.py"
    },
    "auto_claim": {
        "max_retries": 2,
        "retry_interval_minutes": 10,
        "script": "auto-claim-task-v2.py",
        "fallback": "browser_mode"
    },
    "content_reminder": {
        "max_retries": 2,
        "retry_interval_minutes": 5,
        "script": "content_reminder.py"
    },
    "community_reminder": {
        "max_retries": 2,
        "retry_interval_minutes": 5,
        "script": "community_reminder.py"
    },
    "daily_summary": {
        "max_retries": 3,
        "retry_interval_minutes": 10,
        "script": "daily_summary.py"
    }
}

PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def send_feishu_notification(title: str, content: str, status: str = "info"):
    """发送飞书通知"""
    emojis = {"success": "✅", "info": "📋", "warning": "⚠️", "error": "❌"}
    
    try:
        message = f"{emojis.get(status, '📋')} {title}\n\n{content}"
        result = subprocess.Popen(
            ["python3", "/home/admin/.openclaw/workspace/tools/task-notifier.py",
             "start", title, message, "5"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )
        stdout, stderr = result.communicate()
        return result.returncode == 0
    except Exception as e:
        logger.error(f"❌ 通知发送失败：{e}")
        return False


def execute_script(script_name: str) -> bool:
    """执行脚本"""
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        logger.error(f"❌ 脚本不存在：{script_path}")
        return False
    
    try:
        result = subprocess.Popen(
            ["python3", str(script_path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, cwd=str(PROJECT_ROOT)
        )
        stdout, stderr = result.communicate(timeout=300)
        
        if result.returncode == 0:
            logger.info(f"✅ 脚本执行成功：{script_name}")
            return True
        else:
            logger.error(f"❌ 脚本执行失败：{script_name} - {stderr}")
            return False
    
    except Exception as e:
        logger.error(f"❌ 脚本执行异常：{script_name} - {e}")
        return False


def remediate_task(task_name: str, error: str = ""):
    """补救任务执行"""
    logger.info(f"🔧 开始补救任务：{task_name}")
    
    config = REMEDIATION_CONFIG.get(task_name)
    if not config:
        logger.error(f"❌ 未知任务：{task_name}")
        return
    
    max_retries = config["max_retries"]
    script = config["script"]
    
    # 发送补救通知
    send_feishu_notification(
        f"🔧 任务补救执行",
        f"任务：{task_name}\n"
        f"错误：{error}\n"
        f"最大重试：{max_retries} 次",
        "warning"
    )
    
    # 执行补救
    success = False
    for attempt in range(1, max_retries + 1):
        logger.info(f"🔁 补救尝试 {attempt}/{max_retries}")
        
        if execute_script(script):
            success = True
            break
        
        # 等待重试间隔
        if attempt < max_retries:
            import time
            time.sleep(config["retry_interval_minutes"] * 60)
    
    # 发送结果通知
    if success:
        send_feishu_notification(
            f"✅ 任务补救成功",
            f"任务：{task_name}\n"
            f"重试次数：{attempt}/{max_retries}"
        )
    else:
        send_feishu_notification(
            f"❌ 任务补救失败",
            f"任务：{task_name}\n"
            f"重试次数：{max_retries}/{max_retries}\n"
            f"请手动检查",
            "error"
        )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        task_name = sys.argv[1]
        error = sys.argv[2] if len(sys.argv) > 2 else ""
        remediate_task(task_name, error)
    else:
        print("使用：python3 auto-remediation.py <task_name> [error]")
