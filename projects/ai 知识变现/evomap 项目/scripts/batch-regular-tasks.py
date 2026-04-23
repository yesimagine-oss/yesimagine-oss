#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 混合策略批量任务提交
- 批量接普通任务赚积分
- 监控高 bounty 任务刷新
"""

import requests
import time
import json
from datetime import datetime

BASE_URL = "https://evomap.ai"
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ac7f37bf1c5dc13dd375937665839f0fe9396ddfbdf0c36fd450024daf1cc388"
ASSET_ID = "sha256:79e88fcb7b81602d123f3b6b794eed56cb862ecb9feb9df4b474e048f5db531f"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {NODE_SECRET}"
}

def get_available_tasks():
    """获取可接任务"""
    try:
        resp = requests.get(f"{BASE_URL}/a2a/task/list", 
                          headers=HEADERS,
                          params={"limit": 100},
                          timeout=10)
        data = resp.json()
        tasks = data.get('tasks', [])
        available = [t for t in tasks if t.get('claimed_by') is None]
        return available
    except Exception as e:
        print(f"❌ 获取任务失败：{e}")
        return []

def claim_and_submit(task_id):
    """Claim 并提交任务"""
    try:
        # Claim
        claim_resp = requests.post(f"{BASE_URL}/a2a/task/claim",
                                  headers=HEADERS,
                                  json={"task_id": task_id, "node_id": NODE_ID},
                                  timeout=10)
        claim_data = claim_resp.json()
        claim_status = claim_data.get('status', claim_data.get('error', 'ERROR'))
        
        # 提交
        submit_resp = requests.post(f"{BASE_URL}/a2a/task/complete",
                                   headers=HEADERS,
                                   json={"task_id": task_id, "node_id": NODE_ID, "asset_id": ASSET_ID},
                                   timeout=10)
        submit_data = submit_resp.json()
        submit_id = submit_data.get('submission_id', submit_data.get('error', 'ERROR'))
        
        return claim_status, submit_id
    except Exception as e:
        return "ERROR", str(e)

def main():
    print("=" * 60)
    print("🚀 EvoMap 混合策略批量提交")
    print("=" * 60)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"节点 ID: {NODE_ID}")
    print(f"策略：普通任务 + 高 bounty 监控")
    print("=" * 60)
    
    TARGET_REGULAR = 30  # 目标：30 个普通任务
    DELAY = 0.5  # 任务间隔
    HIGH_BOUNTY_THRESHOLD = 50  # 高 bounty 阈值
    
    total_success = 0
    total_failed = 0
    high_bounty_found = 0
    
    # 第 1 阶段：批量接普通任务
    print(f"\n{'='*60}")
    print("📦 第 1 阶段：批量接普通任务")
    print(f"{'='*60}")
    
    tasks = get_available_tasks()
    print(f"✅ 获取到 {len(tasks)} 个可接任务")
    
    # 按 bounty 排序，优先接 bounty 高的
    tasks.sort(key=lambda x: x.get('bounty_amount', 0), reverse=True)
    
    for i, task in enumerate(tasks[:TARGET_REGULAR], 1):
        task_id = task.get('task_id')
        title = task.get('title', 'N/A')[:30]
        bounty = task.get('bounty_amount', 0)
        subs = task.get('submission_count', 0)
        
        emoji = '🔥' if bounty > 100 else '💰' if bounty > 50 else '📝'
        print(f"[{i}/{TARGET_REGULAR}] {emoji} {bounty:3}分 | {title}... ", end="")
        
        claim_status, submit_id = claim_and_submit(task_id)
        
        if submit_id and submit_id != "ERROR" and "error" not in str(submit_id).lower():
            total_success += 1
            if bounty > HIGH_BOUNTY_THRESHOLD:
                high_bounty_found += 1
            print(f"✅ {submit_id[:15]}...")
        else:
            total_failed += 1
            print(f"❌ {claim_status}")
        
        time.sleep(DELAY)
    
    # 第 1 阶段总结
    print(f"\n📊 第 1 阶段完成：成功={total_success}, 失败={total_failed}, 高 bounty={high_bounty_found}")
    
    # 第 2 阶段：监控高 bounty
    print(f"\n{'='*60}")
    print("📡 第 2 阶段：监控高 bounty 任务 (每 5 分钟)")
    print(f"{'='*60}")
    
    monitor_rounds = 4  # 监控 4 轮 = 20 分钟
    
    for round_num in range(1, monitor_rounds + 1):
        print(f"\n🔄 第 {round_num} 轮监控...")
        
        tasks = get_available_tasks()
        high_bounty_tasks = [t for t in tasks if t.get('claimed_by') is None and t.get('bounty_amount', 0) > HIGH_BOUNTY_THRESHOLD]
        
        if high_bounty_tasks:
            print(f"🎯 发现 {len(high_bounty_tasks)} 个高 bounty 任务！")
            
            for task in high_bounty_tasks[:5]:  # 最多接 5 个
                task_id = task.get('task_id')
                bounty = task.get('bounty_amount', 0)
                title = task.get('title', 'N/A')[:30]
                
                print(f"🔥 接高 bounty: {bounty}分 | {title}... ", end="")
                
                claim_status, submit_id = claim_and_submit(task_id)
                
                if submit_id and submit_id != "ERROR":
                    total_success += 1
                    high_bounty_found += 1
                    print(f"✅ {submit_id[:15]}...")
                else:
                    total_failed += 1
                    print(f"❌ {claim_status}")
                
                time.sleep(1)
        else:
            print("⏳ 暂无高 bounty 任务")
        
        if round_num < monitor_rounds:
            print(f"⏱️ 等待 5 分钟...")
            time.sleep(300)  # 5 分钟
    
    # 最终总结
    print("\n" + "=" * 60)
    print("🎉 混合策略执行完成！")
    print("=" * 60)
    print(f"总成功：{total_success} 个")
    print(f"总失败：{total_failed} 个")
    print(f"高 bounty: {high_bounty_found} 个")
    print(f"成功率：{total_success/(total_success+total_failed)*100:.1f}%")
    print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
