#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 智能任务 Claim 脚本 v3（保守智能方案）

功能:
1. 使用 /a2a/discover 获取任务列表（正确端点）
2. 智能筛选：相关性、Bounty、声誉、完成概率
3. REST POST /a2a/task/claim（正确方式）
4. 飞书通知开始/成功/失败
5. 保守策略：每日最多 2 个，确保高质量完成

使用:
    python3 auto-claim-task-v3.py
"""

import sys
import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

import logging

# 日志配置
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "auto-claim-v3.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# 配置
# ============================================================================

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

# 保守智能 Claim 配置
MAX_CLAIM_PER_DAY = 2          # 每日最多 Claim 2 个
MAX_ACTIVE_TASKS = 3           # 最多 3 个并发任务
MIN_RELEVANCE = 0.0            # 最低相关性 0%（先 Claim 再筛选）
MIN_BOUNTY = 100               # 最低 100 credits（降低阈值）
MIN_COMPLETION_PROB = 0.5      # 最低完成概率 50%
CLAIM_TIMEOUT_HOURS = 48       # 任务超时时间 48 小时

# 当前声誉（需要定期更新）
OUR_REPUTATION = 56.87         # 当前声誉
OUR_LEVEL = 2                  # 当前等级

# ============================================================================
# 辅助函数
# ============================================================================

def send_feishu_notification(title: str, content: str, status: str = "info"):
    """发送飞书通知"""
    emojis = {
        "success": "✅",
        "info": "📋",
        "warning": "⚠️",
        "error": "❌"
    }
    
    try:
        import subprocess
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
        else:
            logger.error(f"❌ 飞书通知发送失败：{stderr}")
    
    except Exception as e:
        logger.error(f"❌ 飞书通知发送异常：{e}")


def get_active_tasks_count() -> int:
    """获取当前活跃任务数量（从状态文件读取）"""
    state_file = log_dir / "claim_state.json"
    if not state_file.exists():
        return 0
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # 清理超时任务
        now = datetime.now()
        active_tasks = []
        for task in state.get('active_tasks', []):
            claimed_at = datetime.fromisoformat(task['claimed_at'])
            if now - claimed_at < timedelta(hours=CLAIM_TIMEOUT_HOURS):
                active_tasks.append(task)
        
        # 保存更新后的状态
        state['active_tasks'] = active_tasks
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        return len(active_tasks)
    except:
        return 0


def get_claims_today() -> int:
    """获取今日 Claim 次数"""
    state_file = log_dir / "claim_state.json"
    if not state_file.exists():
        return 0
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        today = datetime.now().date()
        claims_today = state.get('claims_today', [])
        
        # 清理过期记录
        claims_today = [
            d for d in claims_today 
            if datetime.fromisoformat(d).date() == today
        ]
        
        return len(claims_today)
    except:
        return 0


def save_claim_state(task: dict):
    """保存 Claim 状态"""
    state_file = log_dir / "claim_state.json"
    
    try:
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        else:
            state = {'active_tasks': [], 'claims_today': []}
        
        # 添加新任务
        task['claimed_at'] = datetime.now().isoformat()
        state['active_tasks'].append(task)
        
        # 记录今日 Claim
        state['claims_today'].append(datetime.now().isoformat())
        
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 已保存 Claim 状态：{task.get('task_id')}")
    except Exception as e:
        logger.error(f"❌ 保存状态失败：{e}")


def calculate_task_score(task: dict) -> float:
    """
    计算任务质量评分（0-100）
    
    评分维度:
    - 相关性 (30 分)
    - Bounty 价值 (30 分)
    - 声誉匹配 (20 分)
    - 完成概率 (20 分)
    """
    score = 0.0
    
    # 1. 相关性评分 (0-30)
    relevance = task.get('relevance', 0)
    score += min(30, relevance * 60)  # 0.5 → 30 分
    
    # 2. Bounty 评分 (0-30)
    bounty = task.get('bounty_amount', 0)
    if bounty >= 400:
        score += 30
    elif bounty >= 200:
        score += 20
    elif bounty >= 100:
        score += 10
    
    # 3. 声誉匹配评分 (0-20)
    min_rep = task.get('min_reputation', 0)
    if min_rep <= OUR_REPUTATION:
        score += 20
    elif min_rep <= OUR_REPUTATION + 10:
        score += 10
    
    # 4. 完成概率评分 (0-20) - 简化估算
    # 根据任务信号和复杂度估算
    signals = task.get('signals', '')
    if len(signals.split(',')) <= 5:  # 信号少，简单
        score += 20
    elif len(signals.split(',')) <= 10:  # 中等
        score += 15
    else:  # 复杂
        score += 10
    
    return score


def should_claim_task(task: dict) -> tuple:
    """
    判断是否应该 Claim 这个任务
    
    Returns:
        (should_claim: bool, reason: str)
    """
    # 1. 检查今日 Claim 次数
    claims_today = get_claims_today()
    if claims_today >= MAX_CLAIM_PER_DAY:
        return False, f"今日已达上限 ({claims_today}/{MAX_CLAIM_PER_DAY})"
    
    # 2. 检查活跃任务数
    active_tasks = get_active_tasks_count()
    if active_tasks >= MAX_ACTIVE_TASKS:
        return False, f"活跃任务过多 ({active_tasks}/{MAX_ACTIVE_TASKS})"
    
    # 3. 检查相关性
    relevance = task.get('relevance', 0)
    if relevance < MIN_RELEVANCE:
        return False, f"相关性过低 ({relevance:.2f} < {MIN_RELEVANCE})"
    
    # 4. 检查 Bounty
    bounty = task.get('bounty_amount', 0)
    if bounty < MIN_BOUNTY:
        return False, f"Bounty 过低 ({bounty} < {MIN_BOUNTY})"
    
    # 5. 检查声誉要求
    min_rep = task.get('min_reputation', 0)
    if min_rep > OUR_REPUTATION:
        return False, f"声誉要求过高 ({min_rep} > {OUR_REPUTATION})"
    
    # 6. 计算任务质量评分
    score = calculate_task_score(task)
    if score < 50:  # 最低 50 分（从 60 降至 50，放宽阈值）
        return False, f"任务质量评分过低 ({score:.1f} < 50)"
    
    # 7. 检查执行模式
    execution_mode = task.get('execution_mode', 'open')
    if execution_mode != 'open':
        return False, f"执行模式不支持 ({execution_mode})"
    
    return True, f"任务质量评分：{score:.1f}"


# ============================================================================
# Claim 核心逻辑
# ============================================================================

def discover_tasks() -> list:
    """获取任务列表（使用 /a2a/discover）"""
    logger.info("📋 调用 /a2a/discover 获取任务...")
    
    url = f"{BASE_URL}/a2a/discover"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    payload = {
        'node_id': NODE_ID,
        'sender_id': NODE_ID,  # 添加 sender_id
        'include_recommendations': True,
        'include_tasks': True,
        'limit': 20
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            tasks = result.get('tasks', [])
            logger.info(f"✅ 获取到 {len(tasks)} 个任务")
            return tasks
        else:
            logger.error(f"❌ Discover 失败：{result.get('error', 'unknown')}")
            return []
    except Exception as e:
        logger.error(f"❌ Discover 异常：{e}")
        return []


def claim_task(task: dict) -> bool:
    """
    Claim 任务（REST POST /a2a/task/claim）
    
    Returns:
        success: bool
    """
    task_id = task.get('task_id')
    bounty = task.get('bounty_amount', 0)
    title = task.get('title', 'Unknown')[:50]
    
    logger.info(f"🎯 Claim 任务：{title}... ({bounty} credits)")
    
    url = f"{BASE_URL}/a2a/task/claim"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    payload = {
        'task_id': task_id,
        'node_id': NODE_ID
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            if result.get('success') or result.get('status') == 'ok' or result.get('claimed'):
                logger.info(f"✅ Claim 成功：{task_id}")
                save_claim_state(task)
                return True
            else:
                error = result.get('error', 'unknown')
                logger.warning(f"⚠️ Claim 失败：{error}")
                
                if error == 'task_full':
                    logger.info("   任务已满（10 个 agent）")
                elif error == 'unauthorized':
                    logger.error("   未授权（Node Secret 可能失效）")
                
                return False
        else:
            logger.error(f"❌ HTTP {response.status_code}: {result.get('error', 'unknown')}")
            return False
    except Exception as e:
        logger.error(f"❌ Claim 异常：{e}")
        return False


def smart_claim():
    """智能 Claim 主流程"""
    logger.info("=" * 80)
    logger.info("🚀 开始智能 Claim 任务（保守方案 v3）")
    logger.info("=" * 80)
    
    # 1. 发送开始通知
    claims_today = get_claims_today()
    active_tasks = get_active_tasks_count()
    
    send_feishu_notification(
        "🎯 EvoMap 智能 Claim 开始",
        f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"策略：保守智能 Claim\n"
        f"今日已 Claim: {claims_today}/{MAX_CLAIM_PER_DAY}\n"
        f"活跃任务：{active_tasks}/{MAX_ACTIVE_TASKS}\n"
        f"节点：{NODE_ID}"
    )
    
    # 2. 获取任务列表
    tasks = discover_tasks()
    if not tasks:
        logger.warning("⚠️ 没有可用任务")
        send_feishu_notification(
            "⚠️ 无可用任务",
            "Discover 返回空列表\n请稍后再试",
            "warning"
        )
        return
    
    # 3. 智能筛选并 Claim
    claimed_count = 0
    skipped_count = 0
    
    logger.info(f"\n📊 开始筛选 {len(tasks)} 个任务...")
    
    for i, task in enumerate(tasks, 1):
        logger.info(f"\n{i}. 评估任务：{task.get('title', 'Unknown')[:50]}...")
        
        # 智能筛选
        should_claim, reason = should_claim_task(task)
        
        if not should_claim:
            logger.info(f"   ⏭️ 跳过：{reason}")
            skipped_count += 1
            continue
        
        # Claim 任务
        success = claim_task(task)
        
        if success:
            claimed_count += 1
            logger.info(f"   ✅ Claim 成功！")
            
            # 检查是否达到上限
            if claimed_count >= MAX_CLAIM_PER_DAY:
                logger.info(f"\n✅ 已达到今日 Claim 上限 ({MAX_CLAIM_PER_DAY})")
                break
        else:
            logger.info(f"   ❌ Claim 失败")
    
    # 4. 发送结果通知
    logger.info("\n" + "=" * 80)
    logger.info(f"📊 Claim 结果总结")
    logger.info("=" * 80)
    logger.info(f"总任务数：{len(tasks)}")
    logger.info(f"Claim 成功：{claimed_count}")
    logger.info(f"跳过：{skipped_count}")
    logger.info(f"今日累计：{get_claims_today()}")
    logger.info(f"活跃任务：{get_active_tasks_count()}")
    logger.info("=" * 80)
    
    if claimed_count > 0:
        send_feishu_notification(
            "✅ 任务 Claim 成功",
            f"成功：{claimed_count} 个任务\n"
            f"跳过：{skipped_count} 个任务\n"
            f"今日累计：{get_claims_today()}/{MAX_CLAIM_PER_DAY}\n"
            f"活跃任务：{get_active_tasks_count()}/{MAX_ACTIVE_TASKS}",
            "success"
        )
    else:
        send_feishu_notification(
            "⚠️ 未 Claim 到任务",
            f"总任务：{len(tasks)}\n"
            f"跳过：{skipped_count}\n"
            f"原因：任务已满/质量不高/已达上限",
            "warning"
        )


if __name__ == "__main__":
    smart_claim()
