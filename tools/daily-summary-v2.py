#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 每日完成汇总脚本

功能:
1. 统计当日 Claim 任务完成情况
2. 统计当日 Bundle 发布情况
3. 计算声誉变化和积分收益
4. 生成明日目标建议
5. 飞书发送汇总报告

执行时间：每日 23:00

使用:
    python3 daily-summary-v2.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging

# 日志配置
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "daily-summary.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# 配置
# ============================================================================

NODE_ID = "node_67c3b8b37becd262"
CLAIM_STATE_FILE = Path(__file__).parent.parent / "ai 知识变现/evomap 项目/logs/claim_state.json"
BUNDLE_LOG_FILE = Path(__file__).parent.parent / "ai 知识变现/evomap 项目/logs/bundle_publish.log"

# 当前声誉（需要定期更新）
OUR_REPUTATION = 56.87
OUR_LEVEL = 2
NEXT_LEVEL_REPUTATION = 60  # Level 3 需要 60 声誉

# ============================================================================
# 辅助函数
# ============================================================================

def send_feishu_notification(title: str, content: str):
    """发送飞书通知"""
    try:
        import subprocess
        result = subprocess.Popen(
            ["python3", "/home/admin/.openclaw/workspace/tools/task-notifier.py",
             "start", title, content, "5"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = result.communicate(timeout=10)
        
        if result.returncode == 0:
            logger.info("✅ 飞书通知发送成功")
        else:
            logger.error(f"❌ 飞书通知发送失败：{stderr}")
    except Exception as e:
        logger.error(f"❌ 飞书通知发送异常：{e}")


def get_today_claim_stats() -> dict:
    """获取今日 Claim 统计"""
    if not CLAIM_STATE_FILE.exists():
        return {'claimed': 0, 'completed': 0, 'failed': 0, 'bounty': 0}
    
    try:
        with open(CLAIM_STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        today = datetime.now().date()
        history = state.get('history', [])
        
        # 查找今日记录
        today_record = None
        for record in history:
            if datetime.fromisoformat(record['date']).date() == today:
                today_record = record
                break
        
        if not today_record:
            return {'claimed': 0, 'completed': 0, 'failed': 0, 'bounty': 0}
        
        # 计算总 Bounty
        total_bounty = sum(task.get('bounty', 0) for task in today_record.get('tasks', []) 
                          if task.get('status') == 'completed')
        
        return {
            'claimed': today_record.get('claimed_count', 0),
            'completed': today_record.get('completed_count', 0),
            'failed': today_record.get('failed_count', 0),
            'bounty': total_bounty
        }
    except Exception as e:
        logger.error(f"❌ 获取 Claim 统计失败：{e}")
        return {'claimed': 0, 'completed': 0, 'failed': 0, 'bounty': 0}


def get_completion_rate() -> float:
    """计算最近 10 次 Claim 的完成率"""
    if not CLAIM_STATE_FILE.exists():
        return 1.0
    
    try:
        with open(CLAIM_STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        history = state.get('history', [])[-10:]
        if not history:
            return 1.0
        
        completed = sum(h.get('completed_count', 0) for h in history)
        claimed = sum(h.get('claimed_count', 0) for h in history)
        
        return completed / claimed if claimed > 0 else 1.0
    except:
        return 1.0


def get_consecutive_days() -> dict:
    """获取连续工作天数和连续挂零天数"""
    if not CLAIM_STATE_FILE.exists():
        return {'working': 0, 'zero': 0}
    
    try:
        with open(CLAIM_STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        history = state.get('history', [])
        today = datetime.now().date()
        
        # 计算连续工作天数
        working_days = 0
        zero_days = 0
        
        for i in range(30):
            check_date = today - timedelta(days=i)
            day_record = None
            
            for record in history:
                if datetime.fromisoformat(record['date']).date() == check_date:
                    day_record = record
                    break
            
            if day_record and day_record.get('completed_count', 0) > 0:
                working_days += 1
                if zero_days > 0:
                    break
            else:
                zero_days += 1
                if working_days > 0:
                    break
        
        return {'working': working_days, 'zero': zero_days}
    except:
        return {'working': 0, 'zero': 0}


def get_bundle_stats() -> dict:
    """获取 Bundle 发布统计（简化版）"""
    # 实际部署时需要解析 bundle_publish.log
    # 当前返回模拟数据
    return {
        'published': 0,
        'success': 0,
        'bounty': 0
    }


def get_tomorrow_target(completion_rate: float) -> int:
    """根据完成率计算明日目标"""
    if completion_rate >= 0.95:
        return 3
    elif completion_rate >= 0.90:
        return 2
    elif completion_rate >= 0.80:
        return 2
    else:
        return 1


# ============================================================================
# 汇总报告生成
# ============================================================================

def generate_daily_summary() -> str:
    """生成每日汇总报告"""
    logger.info("📊 生成每日汇总报告...")
    
    # 获取统计数据
    claim_stats = get_today_claim_stats()
    completion_rate = get_completion_rate()
    consecutive = get_consecutive_days()
    bundle_stats = get_bundle_stats()
    tomorrow_target = get_tomorrow_target(completion_rate)
    
    # 计算总收益
    total_bounty = claim_stats['bounty'] + bundle_stats['bounty']
    
    # 生成报告
    today = datetime.now().strftime("%Y-%m-%d %A")
    
    report = f"""📅 今日完成汇总 - {today}

🎯 Claim 任务统计
━━━━━━━━━━━━━━━━━━
✅ Claim 成功：{claim_stats['claimed']} 个
✅ 完成提交：{claim_stats['completed']} 个
❌ 失败/超时：{claim_stats['failed']} 个
💰 获得积分：{claim_stats['bounty']} credits
📊 完成率：{completion_rate*100:.1f}%

📦 Bundle 发布统计
━━━━━━━━━━━━━━━━━━
📤 发布数量：{bundle_stats['published']} 个
✅ 成功发布：{bundle_stats['success']} 个
💰 获得积分：{bundle_stats['bounty']} credits

📈 声誉变化
━━━━━━━━━━━━━━━━━━
⭐ 当前声誉：{OUR_REPUTATION}
📊 今日增长：+{claim_stats['completed']*5}
🎯 等级进度：{OUR_REPUTATION}/{NEXT_LEVEL_REPUTATION} (Level {OUR_LEVEL})
📊 升级进度：{(OUR_REPUTATION/NEXT_LEVEL_REPUTATION)*100:.1f}%

🔥 连续记录
━━━━━━━━━━━━━━━━━━
🔥 连续工作：{consecutive['working']} 天
⚠️ 连续挂零：{consecutive['zero']} 天

💡 明日目标
━━━━━━━━━━━━━━━━━━
🎯 建议 Claim: {tomorrow_target} 个
📊 目标完成率：>90%
💰 目标积分：{tomorrow_target*150}+ credits

📊 今日总收益
━━━━━━━━━━━━━━━━━━
💰 总积分：{total_bounty} credits
⭐ 总声誉：+{claim_stats['completed']*5}
⏰ 工作时长：约{claim_stats['completed']*4}小时

━━━━━━━━━━━━━━━━━━
🤖 自动汇总 | 每日 23:00 生成
"""
    
    return report


def generate_simple_summary() -> str:
    """生成简洁版汇总（用于快速查看）"""
    claim_stats = get_today_claim_stats()
    completion_rate = get_completion_rate()
    consecutive = get_consecutive_days()
    
    today = datetime.now().strftime("%m-%d")
    
    simple = f"""😴 {today} 完成汇总

✅ Claim: {claim_stats['claimed']} → {claim_stats['completed']} 个
📊 完成率：{completion_rate*100:.1f}%
💰 积分：+{claim_stats['bounty']}
⭐ 声誉：+{claim_stats['completed']*5}
🔥 连续：{consecutive['working']} 天

{'✅ 达标' if claim_stats['completed'] >= 2 else '⚠️ 继续加油'}
"""
    
    return simple


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("📊 开始生成每日完成汇总")
    logger.info("=" * 80)
    
    # 生成报告
    report = generate_daily_summary()
    simple_report = generate_simple_summary()
    
    # 打印报告
    print("\n" + "=" * 80)
    print(report)
    print("=" * 80)
    
    # 发送飞书通知
    logger.info("\n📱 发送飞书通知...")
    
    # 简洁版（主通知）
    send_feishu_notification(
        "😴 今日完成汇总",
        simple_report
    )
    
    # 详细版（作为后续消息）
    import time
    time.sleep(2)
    
    send_feishu_notification(
        "📅 每日详细报告",
        report
    )
    
    logger.info("\n✅ 每日汇总完成")
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"❌ 汇总生成失败：{e}")
        send_feishu_notification(
            "❌ 每日汇总失败",
            f"错误：{str(e)}\n请检查日志：logs/daily-summary.log"
        )
