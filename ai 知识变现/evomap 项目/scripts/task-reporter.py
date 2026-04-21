#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 定时任务执行汇报脚本

功能:
1. 任务执行后主动汇报
2. 执行结果统计
3. 飞书 + webUI 双渠道通知
4. 日报/周报生成

使用:
    python3 task-reporter.py --task morning_check --status success
    python3 task-reporter.py --daily-summary
"""

import os
import sys
import subprocess
import json
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
        logging.FileHandler(log_dir / "task-reporter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"

# 执行记录文件
EXECUTION_RECORD = LOGS_DIR / "execution_history.json"


def load_execution_history() -> Dict:
    """加载执行历史记录"""
    if EXECUTION_RECORD.exists():
        try:
            with open(EXECUTION_RECORD, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"executions": []}
    return {"executions": []}


def save_execution_history(history: Dict):
    """保存执行历史记录"""
    with open(EXECUTION_RECORD, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def record_execution(task_name: str, status: str, details: str = ""):
    """
    记录任务执行
    
    Args:
        task_name: 任务名称
        status: 执行状态 (success/failed/skipped)
        details: 详细信息
    """
    history = load_execution_history()
    
    record = {
        "timestamp": datetime.now().isoformat(),
        "task": task_name,
        "status": status,
        "details": details
    }
    
    history["executions"].append(record)
    
    # 只保留最近 100 条记录
    if len(history["executions"]) > 100:
        history["executions"] = history["executions"][-100:]
    
    save_execution_history(history)
    logger.info(f"📝 记录执行：{task_name} - {status}")


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


def report_task_execution(task_name: str, status: str, details: str = ""):
    """
    汇报任务执行
    
    Args:
        task_name: 任务名称
        status: 执行状态
        details: 详细信息
    """
    # 记录执行
    record_execution(task_name, status, details)
    
    # 发送通知
    if status == "success":
        send_feishu_notification(
            f"✅ {task_name} 执行成功",
            f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"状态：成功\n"
            f"详情：{details}"
        )
    elif status == "failed":
        send_feishu_notification(
            f"❌ {task_name} 执行失败",
            f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"状态：失败\n"
            f"详情：{details}\n"
            f"请检查日志或手动执行",
            "error"
        )
    elif status == "skipped":
        send_feishu_notification(
            f"⏭️ {task_name} 已跳过",
            f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"状态：跳过\n"
            f"原因：{details}",
            "warning"
        )


def generate_daily_summary():
    """生成每日执行摘要"""
    history = load_execution_history()
    
    # 获取今日记录
    today = datetime.now().strftime("%Y-%m-%d")
    today_records = [
        r for r in history["executions"]
        if r["timestamp"].startswith(today)
    ]
    
    if not today_records:
        logger.info("📊 今日无执行记录")
        return
    
    # 统计
    success_count = sum(1 for r in today_records if r["status"] == "success")
    failed_count = sum(1 for r in today_records if r["status"] == "failed")
    skipped_count = sum(1 for r in today_records if r["status"] == "skipped")
    
    # 生成摘要
    summary = f"""📊 每日执行摘要 - {today}

✅ 成功：{success_count} 个
❌ 失败：{failed_count} 个
⏭️ 跳过：{skipped_count} 个
📝 总计：{len(today_records)} 个

详细记录:
"""
    
    for record in today_records:
        time_str = record["timestamp"].split("T")[1].split(".")[0]
        emoji = "✅" if record["status"] == "success" else "❌" if record["status"] == "failed" else "⏭️"
        summary += f"{emoji} {time_str} {record['task']} - {record['status']}\n"
    
    # 发送摘要
    send_feishu_notification(
        "📊 每日执行摘要",
        summary
    )
    
    logger.info(f"📊 生成每日摘要：{len(today_records)} 条记录")


def generate_weekly_summary():
    """生成每周执行摘要"""
    history = load_execution_history()
    
    # 获取本周记录
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_start_str = week_start.strftime("%Y-%m-%d")
    
    week_records = [
        r for r in history["executions"]
        if r["timestamp"] >= week_start_str
    ]
    
    if not week_records:
        logger.info("📊 本周无执行记录")
        return
    
    # 按天统计
    daily_stats = {}
    for record in week_records:
        day = record["timestamp"].split("T")[0]
        if day not in daily_stats:
            daily_stats[day] = {"success": 0, "failed": 0, "skipped": 0}
        
        status = record["status"]
        if status in daily_stats[day]:
            daily_stats[day][status] += 1
    
    # 生成摘要
    summary = f"""📊 每周执行摘要

周期：{week_start_str} 至 {now.strftime('%Y-%m-%d')}
总执行：{len(week_records)} 次

每日统计:
"""
    
    for day in sorted(daily_stats.keys()):
        stats = daily_stats[day]
        summary += f"{day}: ✅{stats['success']} ❌{stats['failed']} ⏭️{stats['skipped']}\n"
    
    # 发送摘要
    send_feishu_notification(
        "📊 每周执行摘要",
        summary
    )
    
    logger.info(f"📊 生成每周摘要：{len(week_records)} 条记录")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="任务执行汇报工具")
    parser.add_argument("--task", type=str, help="任务名称")
    parser.add_argument("--status", type=str, choices=["success", "failed", "skipped"], help="执行状态")
    parser.add_argument("--details", type=str, default="", help="详细信息")
    parser.add_argument("--daily-summary", action="store_true", help="生成每日摘要")
    parser.add_argument("--weekly-summary", action="store_true", help="生成每周摘要")
    
    args = parser.parse_args()
    
    if args.daily_summary:
        generate_daily_summary()
    elif args.weekly_summary:
        generate_weekly_summary()
    elif args.task and args.status:
        report_task_execution(args.task, args.status, args.details)
    else:
        parser.print_help()
