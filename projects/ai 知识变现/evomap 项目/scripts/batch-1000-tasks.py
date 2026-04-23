#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 批量 1000 任务提交脚本
分批次执行，避免速率限制
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

def get_available_tasks(limit=500):
    """获取可接任务列表"""
    try:
        resp = requests.get(f"{BASE_URL}/a2a/task/list", 
                          headers=HEADERS,
                          params={"limit": limit})
        data = resp.json()
        tasks = data.get('tasks', [])
        
        # 筛选未被 claim 的任务
        available = [t for t in tasks if t.get('claimed_by') is None]
        
        # 按提交数排序（少的优先）
        available.sort(key=lambda x: x.get('submission_count', 0))
        
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
                                  json={"task_id": task_id, "node_id": NODE_ID})
        claim_data = claim_resp.json()
        claim_status = claim_data.get('status', claim_data.get('error', 'ERROR'))
        
        # 提交
        submit_resp = requests.post(f"{BASE_URL}/a2a/task/complete",
                                   headers=HEADERS,
                                   json={"task_id": task_id, "node_id": NODE_ID, "asset_id": ASSET_ID})
        submit_data = submit_resp.json()
        submit_id = submit_data.get('submission_id', submit_data.get('error', 'ERROR'))
        
        return claim_status, submit_id
    except Exception as e:
        return "ERROR", str(e)

def main():
    print("=" * 60)
    print("🚀 EvoMap 1000 任务批量提交")
    print("=" * 60)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"节点 ID: {NODE_ID}")
    print(f"目标：1000 个任务")
    print("=" * 60)
    
    TARGET = 1000
    BATCH_SIZE = 50  # 每批 50 个
    DELAY = 0.5  # 每个任务间隔 0.5 秒
    
    total_success = 0
    total_failed = 0
    batch_num = 0
    
    while total_success + total_failed < TARGET:
        batch_num += 1
        print(f"\n{'='*60}")
        print(f"📦 第 {batch_num} 批")
        print(f"{'='*60}")
        
        # 获取任务
        print("📋 获取任务列表...")
        tasks = get_available_tasks(limit=500)
        
        if not tasks:
            print("❌ 没有可接任务了！")
            break
        
        # 计算本批数量
        remaining = TARGET - (total_success + total_failed)
        batch_tasks = tasks[:min(BATCH_SIZE, remaining, len(tasks))]
        
        print(f"✅ 获取到 {len(tasks)} 个可接任务")
        print(f"📦 本批处理 {len(batch_tasks)} 个任务")
        print(f"📊 进度：{total_success + total_failed}/{TARGET}")
        print()
        
        # 处理本批任务
        batch_success = 0
        batch_failed = 0
        
        for i, task in enumerate(batch_tasks, 1):
            task_id = task.get('task_id')
            title = task.get('title', 'N/A')[:30]
            subs = task.get('submission_count', 0)
            
            print(f"[{i}/{len(batch_tasks)}] {title}... ({subs}提交)", end=" → ")
            
            claim_status, submit_id = claim_and_submit(task_id)
            
            if submit_id and submit_id != "ERROR" and "error" not in str(submit_id).lower():
                batch_success += 1
                total_success += 1
                print(f"✅ {submit_id[:20]}...")
            else:
                batch_failed += 1
                total_failed += 1
                print(f"❌ {claim_status}")
            
            # 延迟避免限流
            time.sleep(DELAY)
        
        # 批次总结
        print(f"\n📊 第 {batch_num} 批完成：成功={batch_success}, 失败={batch_failed}")
        
        # 批次间延迟更长
        if batch_success + batch_failed >= TARGET:
            break
        
        print("⏱️ 等待 5 秒，继续下一批...")
        time.sleep(5)
    
    # 最终总结
    print("\n" + "=" * 60)
    print("🎉 全部完成！")
    print("=" * 60)
    print(f"总成功：{total_success} 个")
    print(f"总失败：{total_failed} 个")
    print(f"成功率：{total_success/(total_success+total_failed)*100:.1f}%")
    print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
