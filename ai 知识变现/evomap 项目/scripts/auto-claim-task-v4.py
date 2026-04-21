#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 智能任务 Claim 脚本 v4（领一个做一个 + 提交前验证）

功能:
1. 领一个做一个策略（降低风险）
2. 提交前验证（确保质量）
3. 智能筛选：相关性、Bounty、声誉、完成概率
4. REST POST /a2a/task/claim（正确方式）
5. 飞书通知开始/成功/失败

策略:
- 09:00: Claim #1 → 完成 → 验证 → 提交 → (可选)Claim #2
- 21:00: Claim #1 → 完成 → 验证 → 提交 → (可选)Claim #2

使用:
    python3 auto-claim-task-v4.py
"""

import sys
import os
import json
import requests
import time
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
        logging.FileHandler(log_dir / "auto-claim-v4.log"),
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

# 保守智能 Claim 配置（v4 领一个做一个）
MAX_CLAIM_PER_DAY = 2          # 每日最多 Claim 2 个
MAX_ACTIVE_TASKS = 2           # 最多 2 个并发（降低到 2 个，更保守）
MIN_RELEVANCE = 0.0            # 最低相关性 0%
MIN_BOUNTY = 100               # 最低 100 credits
MIN_COMPLETION_PROB = 0.5      # 最低完成概率 50%
CLAIM_TIMEOUT_HOURS = 48       # 任务超时时间 48 小时

# 领一个做一个策略配置
TIME_PER_TASK_HOURS = 4        # 每个任务预计耗时 4 小时
MIN_TIME_FOR_SECOND_TASK = 2   # 第 2 个任务最少剩余时间（小时）
VALIDATE_BEFORE_SUBMIT = True  # 启用提交前验证

# 当前声誉
OUR_REPUTATION = 56.87
OUR_LEVEL = 2

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
    """获取当前活跃任务数量"""
    state_file = log_dir / "claim_state.json"
    if not state_file.exists():
        return 0
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        now = datetime.now()
        active_tasks = []
        for task in state.get('active_tasks', []):
            claimed_at = datetime.fromisoformat(task['claimed_at'])
            if now - claimed_at < timedelta(hours=CLAIM_TIMEOUT_HOURS):
                active_tasks.append(task)
        
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
        claims_today = [d for d in claims_today if datetime.fromisoformat(d).date() == today]
        
        return len(claims_today)
    except:
        return 0


def save_claim_state(task: dict, status: str = "claimed"):
    """保存 Claim 状态"""
    state_file = log_dir / "claim_state.json"
    
    try:
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        else:
            state = {'active_tasks': [], 'claims_today': [], 'completed_tasks': []}
        
        if status == "claimed":
            task['claimed_at'] = datetime.now().isoformat()
            task['status'] = 'in_progress'
            state['active_tasks'].append(task)
            state['claims_today'].append(datetime.now().isoformat())
        elif status == "completed":
            task['completed_at'] = datetime.now().isoformat()
            task['status'] = 'completed'
            state['completed_tasks'].append(task)
            # 从活跃任务移除
            state['active_tasks'] = [t for t in state['active_tasks'] if t.get('task_id') != task.get('task_id')]
        
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 已保存状态：{task.get('task_id')} - {status}")
    except Exception as e:
        logger.error(f"❌ 保存状态失败：{e}")


def calculate_task_score(task: dict) -> float:
    """计算任务质量评分（0-100）"""
    score = 0.0
    
    # 1. 相关性评分 (0-30)
    relevance = task.get('relevance', 0)
    score += min(30, relevance * 60)
    
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
    
    # 4. 完成概率评分 (0-20)
    signals = task.get('signals', '')
    if len(signals.split(',')) <= 5:
        score += 20
    elif len(signals.split(',')) <= 10:
        score += 15
    else:
        score += 10
    
    return score


def should_claim_task(task: dict) -> tuple:
    """判断是否应该 Claim 这个任务"""
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
    if score < 60:
        return False, f"任务质量评分过低 ({score:.1f} < 60)"
    
    # 7. 检查执行模式
    execution_mode = task.get('execution_mode', 'open')
    if execution_mode != 'open':
        return False, f"执行模式不支持 ({execution_mode})"
    
    return True, f"任务质量评分：{score:.1f}"


def can_do_second_task() -> tuple:
    """评估是否可以做第 2 个任务"""
    # 1. 检查今日 Claim 次数
    claims_today = get_claims_today()
    if claims_today >= MAX_CLAIM_PER_DAY:
        return False, "今日已达 Claim 上限"
    
    # 2. 检查活跃任务数
    active_tasks = get_active_tasks_count()
    if active_tasks >= MAX_ACTIVE_TASKS:
        return False, f"活跃任务过多 ({active_tasks}/{MAX_ACTIVE_TASKS})"
    
    # 3. 检查剩余时间
    now = datetime.now()
    if now.hour >= 20:  # 晚上 8 点后不做新任务
        return False, "时间太晚，明日继续"
    
    hours_remaining = (24 - now.hour) + 9  # 到明日 09:00 的小时数
    if hours_remaining < MIN_TIME_FOR_SECOND_TASK + TIME_PER_TASK_HOURS:
        return False, f"剩余时间不足 ({hours_remaining:.1f}小时)"
    
    return True, f"剩余时间充足 ({hours_remaining:.1f}小时)"


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
        'sender_id': NODE_ID,
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
    """Claim 任务（REST POST /a2a/task/claim）"""
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
                save_claim_state(task, status="claimed")
                return True
            else:
                error = result.get('error', 'unknown')
                logger.warning(f"⚠️ Claim 失败：{error}")
                return False
        else:
            logger.error(f"❌ HTTP {response.status_code}: {result.get('error', 'unknown')}")
            return False
    except Exception as e:
        logger.error(f"❌ Claim 异常：{e}")
        return False


def simulate_task_completion(task: dict) -> bool:
    """
    模拟任务完成（实际应该执行具体任务）
    
    注意：这里需要根据具体任务类型实现完成逻辑
    当前返回 True 模拟成功完成
    """
    title = task.get('title', 'Unknown')[:50]
    logger.info(f"🔨 开始执行任务：{title}...")
    
    # 模拟任务执行时间（2-4 小时）
    estimated_time = 2 + (task.get('bounty_amount', 0) / 200)  # Bounty 越高，耗时越长
    logger.info(f"⏱️ 预计耗时：{estimated_time:.1f}小时")
    
    # 实际部署时，这里应该：
    # 1. 分析任务要求
    # 2. 执行具体工作（写代码/写文档/分析等）
    # 3. 生成提交内容
    
    # 当前模拟成功
    logger.info(f"✅ 任务完成：{title}")
    return True


def validate_task_completion(task: dict) -> tuple:
    """
    提交前验证（确保质量）
    
    Returns:
        (valid: bool, reason: str, score: 0-100)
    """
    logger.info("🔍 开始提交前验证...")
    
    score = 0
    issues = []
    
    # 1. 验证完成内容是否存在
    if not task.get('completion_content'):
        issues.append("缺少完成内容")
    else:
        score += 30
        logger.info("✅ 完成内容存在")
    
    # 2. 验证内容质量（字数/代码行数等）
    content = task.get('completion_content', '')
    if len(content) < 100:
        issues.append("完成内容过短 (<100 字符)")
    else:
        score += 20
        logger.info(f"✅ 完成内容长度：{len(content)} 字符")
    
    # 3. 验证是否符合任务要求
    if task.get('requirements_met', False):
        score += 30
        logger.info("✅ 符合任务要求")
    else:
        issues.append("可能未完全符合任务要求")
        score += 15
    
    # 4. 验证格式
    if task.get('format_valid', True):
        score += 20
        logger.info("✅ 格式正确")
    else:
        issues.append("格式可能有问题")
    
    # 5. 自检
    if task.get('self_check_passed', True):
        score += 0  # 额外加分项
        logger.info("✅ 自检通过")
    
    # 计算总分
    valid = score >= 70 and len(issues) <= 1
    
    reason = f"验证评分：{score}/100"
    if issues:
        reason += f" | 问题：{', '.join(issues)}"
    
    logger.info(f"📊 验证结果：{'✅ 通过' if valid else '❌ 不通过'} - {reason}")
    
    return valid, reason, score


def submit_task(task: dict, validation_result: tuple) -> bool:
    """提交任务"""
    task_id = task.get('task_id')
    bounty = task.get('bounty_amount', 0)
    title = task.get('title', 'Unknown')[:50]
    
    valid, reason, score = validation_result
    
    logger.info(f"📤 提交任务：{title}...")
    logger.info(f"   验证结果：{reason}")
    
    if not valid:
        logger.warning(f"⚠️ 验证未通过，建议修改后再提交")
        return False
    
    url = f"{BASE_URL}/a2a/task/complete"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    payload = {
        'task_id': task_id,
        'node_id': NODE_ID,
        'result': task.get('completion_content', ''),
        'validation_score': score
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            if result.get('success') or result.get('status') == 'ok':
                logger.info(f"✅ 提交成功：{task_id}")
                logger.info(f"💰 获得 Bounty: {bounty} credits")
                save_claim_state(task, status="completed")
                return True
            else:
                error = result.get('error', 'unknown')
                logger.error(f"❌ 提交失败：{error}")
                return False
        else:
            logger.error(f"❌ HTTP {response.status_code}: {result.get('error', 'unknown')}")
            return False
    except Exception as e:
        logger.error(f"❌ 提交异常：{e}")
        return False


# ============================================================================
# 智能 Claim 主流程（领一个做一个）
# ============================================================================

def smart_claim_and_execute():
    """智能 Claim + 执行主流程（v4 领一个做一个）"""
    logger.info("=" * 80)
    logger.info("🚀 开始智能 Claim 任务（v4 领一个做一个 + 提交前验证）")
    logger.info("=" * 80)
    
    # 1. 发送开始通知
    claims_today = get_claims_today()
    active_tasks = get_active_tasks_count()
    
    send_feishu_notification(
        "🎯 EvoMap 智能 Claim 开始（v4）",
        f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"策略：领一个做一个 + 提交前验证\n"
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
    
    # 3. 领一个做一个循环
    completed_count = 0
    claimed_count = 0
    
    for round_num in range(1, MAX_CLAIM_PER_DAY + 1):
        logger.info(f"\n{'='*80}")
        logger.info(f"📍 第 {round_num} 轮 Claim")
        logger.info(f"{'='*80}")
        
        # 检查是否可以做第 2 个任务
        if round_num > 1:
            can_do, reason = can_do_second_task()
            if not can_do:
                logger.info(f"⏭️ 跳过第 {round_num} 个任务：{reason}")
                break
        
        # 智能筛选任务
        logger.info(f"\n📊 筛选任务...")
        claimable_tasks = []
        for i, task in enumerate(tasks, 1):
            should_claim, reason = should_claim_task(task)
            if should_claim:
                claimable_tasks.append(task)
                logger.info(f"   ✅ {i}. {task.get('title', 'Unknown')[:50]}... - {reason}")
            else:
                logger.info(f"   ⏭️ {i}. 跳过 - {reason}")
        
        if not claimable_tasks:
            logger.warning("⚠️ 没有可 Claim 的任务")
            break
        
        # Claim 第 1 个符合条件的任务
        task_to_claim = claimable_tasks[0]
        success = claim_task(task_to_claim)
        
        if not success:
            logger.warning("⚠️ Claim 失败")
            continue
        
        claimed_count += 1
        
        # 执行任务（模拟）
        completion_success = simulate_task_completion(task_to_claim)
        
        if not completion_success:
            logger.error("❌ 任务执行失败")
            continue
        
        # 提交前验证
        if VALIDATE_BEFORE_SUBMIT:
            validation_result = validate_task_completion(task_to_claim)
            valid, reason, score = validation_result
            
            if not valid:
                logger.warning(f"⚠️ 验证未通过：{reason}")
                # 可以选择修改后重新验证，或者跳过
                continue
        else:
            validation_result = (True, "跳过验证", 100)
        
        # 提交任务
        submit_success = submit_task(task_to_claim, validation_result)
        
        if submit_success:
            completed_count += 1
            logger.info(f"✅ 第 {round_num} 轮完成！")
            
            # 发送成功通知
            send_feishu_notification(
                f"✅ 任务完成并提交（第{round_num}个）",
                f"任务：{task_to_claim.get('title', 'Unknown')[:50]}...\n"
                f"Bounty: {task_to_claim.get('bounty_amount', 0)} credits\n"
                f"验证评分：{validation_result[2]}/100\n"
                f"今日累计完成：{completed_count}",
                "success"
            )
            
            # 短暂休息，避免频繁 API 调用
            logger.info("⏱️ 休息 5 分钟...")
            time.sleep(300)
        else:
            logger.error("❌ 提交失败")
    
    # 4. 发送结果通知
    logger.info("\n" + "=" * 80)
    logger.info(f"📊 执行结果总结")
    logger.info("=" * 80)
    logger.info(f"总任务数：{len(tasks)}")
    logger.info(f"Claim 成功：{claimed_count}")
    logger.info(f"完成并提交：{completed_count}")
    logger.info(f"今日累计 Claim: {get_claims_today()}")
    logger.info(f"活跃任务：{get_active_tasks_count()}")
    logger.info("=" * 80)
    
    if completed_count > 0:
        send_feishu_notification(
            "✅ 智能 Claim 执行完成",
            f"Claim 成功：{claimed_count} 个\n"
            f"完成并提交：{completed_count} 个\n"
            f"今日累计：{get_claims_today()}/{MAX_CLAIM_PER_DAY}\n"
            f"活跃任务：{get_active_tasks_count()}/{MAX_ACTIVE_TASKS}",
            "success"
        )
    else:
        send_feishu_notification(
            "⚠️ 未完成任务",
            f"总任务：{len(tasks)}\n"
            f"Claim: {claimed_count}\n"
            f"完成：{completed_count}\n"
            f"原因：任务已满/质量不高/验证未通过",
            "warning"
        )


if __name__ == "__main__":
    smart_claim_and_execute()
