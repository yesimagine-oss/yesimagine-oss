#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 每日晚间汇总脚本
每天 22:00 执行，合并 EvoMap 数据 + 工作汇报 + 事故反思
"""

import requests
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
EVO_API = "https://evomap.ai"
WORKSPACE = Path("/home/admin/.openclaw/workspace")

# 日志配置
log_dir = WORKSPACE / "EvoMap 项目" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "cron_daily.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ==================== EvoMap 数据 ====================

def get_my_tasks() -> List[Dict]:
    """获取我的任务"""
    try:
        response = requests.get(
            f"{EVO_API}/a2a/task/my?node_id={NODE_ID}",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('tasks', [])
    except Exception as e:
        logger.error(f"获取任务失败：{e}")
    return []


def get_evomap_stats():
    """获取 EvoMap 统计数据"""
    tasks = get_my_tasks()
    
    completed = len([t for t in tasks if t.get('status') == 'completed'])
    submitted = len([t for t in tasks if t.get('my_submission_status') == 'pending'])
    rejected = len([t for t in tasks if t.get('my_submission_status') == 'rejected'])
    
    # 获取今日提交的任务
    today = datetime.now().strftime('%Y-%m-%d')
    today_tasks = []
    for task in tasks:
        # 简单判断：今天创建或提交的任务
        created_at = task.get('created_at', '')
        if today in created_at:
            today_tasks.append(task)
    
    return {
        'total_tasks': len(tasks),
        'completed': completed,
        'submitted': submitted,
        'rejected': rejected,
        'today_tasks': today_tasks,
    }


# ==================== 工作日志 ====================

def get_work_log() -> Dict:
    """获取今日工作记录"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 读取今日 memory 文件
    memory_file = WORKSPACE / "memory" / f"{today}.md"
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 简单解析（后续可优化）
            return {
                'completed': extract_completed_tasks(content),
                'incomplete': extract_incomplete_tasks(content),
            }
    
    return {'completed': [], 'incomplete': []}


def extract_completed_tasks(content: str) -> List[str]:
    """提取已完成任务"""
    tasks = []
    for line in content.split('\n'):
        if line.strip().startswith('✅'):
            tasks.append(line.strip())
    return tasks[:10]  # 最多 10 条


def extract_incomplete_tasks(content: str) -> List[str]:
    """提取未完成任务"""
    tasks = []
    for line in content.split('\n'):
        if line.strip().startswith('❌') or line.strip().startswith('⏳'):
            tasks.append(line.strip())
    return tasks[:10]


# ==================== 事故记录 ====================

def get_accidents() -> List[Dict]:
    """获取今日事故记录"""
    today = datetime.now().strftime('%Y-%m-%d')
    accidents_dir = WORKSPACE / ".learnings"
    
    accidents = []
    if accidents_dir.exists():
        for file in accidents_dir.glob(f"{today}*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    accidents.append({
                        'file': file.name,
                        'summary': content[:200] + '...' if len(content) > 200 else content,
                    })
            except Exception as e:
                logger.error(f"读取事故记录失败：{e}")
    
    return accidents


# ==================== 定时任务状态 ====================

def get_cron_status() -> List[Dict]:
    """获取定时任务执行状态"""
    cron_tasks = [
        {'time': '07:30', 'name': '晨间检查', 'log': 'cron_morning.log'},
        {'time': '17:25', 'name': '任务提醒', 'log': 'cron_task.log'},
        {'time': '17:30', 'name': '自动 Claim', 'log': 'auto-claim.log'},
        {'time': '18:10', 'name': '创作提醒', 'log': 'cron_content.log'},
        {'time': '20:00', 'name': '社区互动', 'log': 'cron_community.log'},
        {'time': '22:00', 'name': '每日汇总', 'log': 'cron_daily.log'},
    ]
    
    for task in cron_tasks:
        log_file = log_dir / task['log']
        if log_file.exists():
            # 检查今日是否有执行记录
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                today = datetime.now().strftime('%Y-%m-%d')
                task['status'] = '✅ 已执行' if today in content else '❌ 未执行'
        else:
            task['status'] = '❌ 无日志'
    
    return cron_tasks


# ==================== 生成报告 ====================

def generate_report():
    """生成合并报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 获取数据
    evomap_stats = get_evomap_stats()
    work_log = get_work_log()
    accidents = get_accidents()
    cron_status = get_cron_status()
    
    # 生成报告
    report = f"""# 📋 每日晚间汇总 — {today}

━━━━━━━━━━━━━━━━━━━━

## 1️⃣ EvoMap 项目

### 📊 今日数据

| 项目 | 数值 | 说明 |
|------|------|------|
| **总任务数** | {evomap_stats['total_tasks']} | 所有相关任务 |
| **已完成** | {evomap_stats['completed']} | 已提交并完成 |
| **审核中** | {evomap_stats['submitted']} | 等待审核 |
| **被拒绝** | {evomap_stats['rejected']} | 需要改进 |

### ✅ 今日任务
"""
    
    # 今日任务详情
    if evomap_stats['today_tasks']:
        for task in evomap_stats['today_tasks'][:5]:
            title = task.get('title', '未知任务')[:50]
            status = task.get('my_submission_status', 'unknown')
            report += f"- {title} [`{status}`]\n"
    else:
        report += "- 无今日新任务\n"
    
    report += f"""
### 📋 定时任务执行情况

| 时间 | 任务 | 状态 |
|------|------|------|
"""
    
    for task in cron_status:
        report += f"| {task['time']} | {task['name']} | {task['status']} |\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━

## 2️⃣ 其他工作

### ✅ 完成任务
"""
    
    if work_log['completed']:
        for task in work_log['completed'][:5]:
            report += f"{task}\n"
    else:
        report += "- 无记录\n"
    
    report += f"""
### ⏳ 未完成
"""
    
    if work_log['incomplete']:
        for task in work_log['incomplete'][:5]:
            report += f"{task}\n"
    else:
        report += "- 无\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━

## 3️⃣ 事故与反思
"""
    
    if accidents:
        for acc in accidents:
            report += f"\n### 🚨 {acc['file']}\n"
            report += f"{acc['summary']}\n"
    else:
        report += "\n✅ 无事故记录\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━

## 4️⃣ 明日计划

📌 {datetime.now().strftime('%Y-%m-%d')} 重点：
- [ ] 严格执行 EvoMap 每日任务（Claim + 创作 + 社区）
- [ ] 跟进已提交任务的审核结果
- [ ] 主动汇报进度，不等用户询问
- [ ] 零事故、零推卸、零装傻

━━━━━━━━━━━━━━━━━━━━

## 5️⃣ 今日评分

⚠️ 自评：待用户评分
🎯 明日目标：100/100（严格执行，零事故）

━━━━━━━━━━━━━━━━━━━━

**报告人：** RedOpenClaw  
**发送时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

晚安！🌙
"""
    
    return report


# ==================== 发送报告 ====================

def send_feishu_report(report: str):
    """发送飞书报告"""
    try:
        import subprocess
        
        # 使用 task-notifier.py 发送（Python 3.6 兼容）
        result = subprocess.Popen(
            ["python3", str(WORKSPACE / "tools" / "task-notifier.py"),
             "end", "每日晚间汇总", report, "5"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = result.communicate()
        
        if result.returncode == 0:
            logger.info("✅ 飞书报告发送成功")
            return True
        else:
            logger.error(f"❌ 飞书报告发送失败：{stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 飞书报告发送异常：{e}")
        return False


def save_to_memory(report: str):
    """保存到 memory 文件"""
    today = datetime.now().strftime('%Y-%m-%d')
    memory_file = WORKSPACE / "memory" / f"{today}.md"
    
    try:
        # 追加到 memory 文件
        with open(memory_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n---\n\n## 晚间汇总（{datetime.now().strftime('%H:%M')}）\n\n")
            f.write(report)
        logger.info("✅ 已保存到 memory 文件")
    except Exception as e:
        logger.error(f"❌ 保存到 memory 失败：{e}")


# ==================== 主函数 ====================

def main():
    """主函数"""
    logger.info("📊 开始执行每日晚间汇总...")
    
    # 生成报告
    report = generate_report()
    
    # 发送飞书
    send_feishu_report(report)
    
    # 保存到 memory
    save_to_memory(report)
    
    # 输出到日志
    print(report)
    
    logger.info("✅ 每日晚间汇总执行完成")


if __name__ == "__main__":
    main()
