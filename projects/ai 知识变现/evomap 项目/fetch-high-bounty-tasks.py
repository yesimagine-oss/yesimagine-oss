#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取高分值悬赏任务
目标：找到 50+ 积分的任务，优先做
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 清除代理
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

# 节点配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

def fetch_and_analyze_tasks(client):
    """获取并分析任务"""
    print("\n" + "="*80)
    print("获取高分值悬赏任务")
    print("="*80)
    
    # 获取任务（通过 heartbeat）
    url = f"{BASE_URL}/a2a/heartbeat"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    payload = {'node_id': NODE_ID}
    
    import requests
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    if response.status_code != 200:
        print(f"❌ 获取失败：HTTP {response.status_code}")
        return [], []
    
    result = response.json()
    
    # 分析 available_tasks
    available_tasks = result.get('available_tasks', [])
    available_work = result.get('available_work', [])
    
    print(f"\n✅ 找到 {len(available_tasks)} 个 available_tasks")
    print(f"✅ 找到 {len(available_work)} 个 available_work")
    
    # 筛选高分值任务
    high_bounty_tasks = []
    
    for task in available_tasks:
        bounty = float(task.get('bounty_amount', 0))
        if bounty >= 50:
            high_bounty_tasks.append({
                'source': 'available_tasks',
                'task': task,
                'bounty': bounty
            })
    
    for work in available_work:
        bounty = float(work.get('bountyAmount', 0))
        if bounty >= 50:
            high_bounty_tasks.append({
                'source': 'available_work',
                'task': work,
                'bounty': bounty
            })
    
    # 按赏金排序
    high_bounty_tasks.sort(key=lambda x: x['bounty'], reverse=True)
    
    return high_bounty_tasks, result

def print_task_details(tasks, result):
    """打印任务详情"""
    
    # 打印当前积分
    credit_balance = result.get('credit_balance', 0)
    print(f"\n当前积分：{credit_balance} 积分")
    print(f"目标积分：2000 积分（Premium）")
    print(f"缺口：{2000 - credit_balance:.0f} 积分")
    
    # 打印高分值任务
    print("\n" + "="*80)
    print("高分值任务（50+ 积分）")
    print("="*80)
    
    if not tasks:
        print("\n❌ 没有找到高分值任务")
        return
    
    print(f"\n共找到 {len(tasks)} 个高分值任务\n")
    
    # 分组打印
    tiers = {
        '500+': [t for t in tasks if t['bounty'] >= 500],
        '300-499': [t for t in tasks if 300 <= t['bounty'] < 500],
        '200-299': [t for t in tasks if 200 <= t['bounty'] < 300],
        '100-199': [t for t in tasks if 100 <= t['bounty'] < 200],
        '50-99': [t for t in tasks if 50 <= t['bounty'] < 100],
    }
    
    for tier_name, tier_tasks in tiers.items():
        if not tier_tasks:
            continue
        
        print(f"\n{'='*80}")
        print(f"{tier_name} 积分档（{len(tier_tasks)} 个任务）")
        print(f"{'='*80}")
        
        for i, item in enumerate(tier_tasks[:10]):  # 每档最多显示 10 个
            task = item['task']
            bounty = item['bounty']
            source = item['source']
            
            # 获取任务信息
            task_id = task.get('task_id') or task.get('id')
            title = task.get('title', '无标题')
            signals = task.get('signals', '')
            min_rep = task.get('min_reputation', 0) or task.get('minReputation', 0)
            expires = task.get('expires_at', '')
            submission_count = task.get('submission_count', 0)
            slots = task.get('slots_remaining', 'N/A')
            
            # 检查是否符合资格
            our_rep = 50  # 当前声誉
            eligible = "✅" if our_rep >= min_rep else "❌"
            
            print(f"\n{i+1}. [{eligible}] {title[:80]}")
            print(f"   赏金：{bounty:.0f} 积分")
            print(f"   最低声誉：{min_rep}（我们：{our_rep}）")
            print(f"   信号：{signals[:100] if signals else '无'}")
            if expires:
                print(f"   到期：{expires[:19]}")
            print(f"   提交：{submission_count} 个，剩余：{slots} 个位置")
            print(f"   来源：{source}")

def recommend_tasks(tasks):
    """推荐任务"""
    print("\n" + "="*80)
    print("推荐任务（按优先级）")
    print("="*80)
    
    # 筛选符合资格的任务
    our_rep = 50
    eligible_tasks = [t for t in tasks if t['task'].get('min_reputation', 0) or t['task'].get('minReputation', 0) <= our_rep]
    
    if not eligible_tasks:
        print("\n❌ 没有符合资格的任务")
        return
    
    # 按赏金排序，取前 5 个
    eligible_tasks.sort(key=lambda x: x['bounty'], reverse=True)
    top_tasks = eligible_tasks[:5]
    
    print(f"\n推荐做以下 {len(top_tasks)} 个任务：\n")
    
    total_bounty = 0
    for i, item in enumerate(top_tasks):
        task = item['task']
        bounty = item['bounty']
        total_bounty += bounty
        
        title = task.get('title', '无标题')[:60]
        signals = task.get('signals', '')[:50]
        
        print(f"{i+1}. {title}...")
        print(f"   赏金：{bounty:.0f} 积分 | 信号：{signals}")
    
    print(f"\n预计收益：{total_bounty:.0f} 积分")
    print(f"完成后可达：{total_bounty + 2.56:.0f} 积分")
    print(f"距离 Premium 还差：{2000 - total_bounty - 2.56:.0f} 积分")

# 主程序
print("="*80)
print("EvoMap 高分值任务获取")
print("="*80)
print(f"节点：{NODE_ID}")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 初始化客户端
client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)

# 认证
print("\n[1/3] 认证...")
hello_result = client.hello()
if not hello_result.get('success'):
    print(f"❌ 认证失败：{hello_result.get('error')}")
    sys.exit(1)

print(f"✅ 认证成功")

# 获取任务
print(f"\n[2/3] 获取高分值任务...")
high_bounty_tasks, result = fetch_and_analyze_tasks(client)

# 打印详情
print(f"\n[3/3] 分析任务...")
print_task_details(high_bounty_tasks, result)

# 推荐
recommend_tasks(high_bounty_tasks)

print(f"\n{'='*80}")
print(f"下一步：")
print(f"1. 选择 1-2 个任务开始做")
print(f"2. 完成后提交结果")
print(f"3. 重复直到达到 2000 积分")
print(f"{'='*80}")
