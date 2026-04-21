#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
领取第 1 个高分值任务
任务：AI NPC 对话系统硬件指南（493 积分）
"""

import json
import sys
import os
import requests
from pathlib import Path
from datetime import datetime

# 清除代理
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

# 节点配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

# 任务信息
TASK_ID = "cmc94c07136ffdfc311f9983c"
TASK_TITLE = "What hardware and setup is optimal for AI NPC dialogue systems with dynamic personality?"
BOUNTY_AMOUNT = 493
BOUNTY_ID = "cm513197141335f60072f0baa"

def claim_task():
    """领取任务"""
    print("\n" + "="*80)
    print("领取任务")
    print("="*80)
    
    print(f"\n任务信息:")
    print(f"  ID: {TASK_ID}")
    print(f"  标题：{TASK_TITLE[:80]}...")
    print(f"  赏金：{BOUNTY_AMOUNT} 积分")
    print(f"  悬赏 ID: {BOUNTY_ID}")
    
    # 领取任务端点
    url = f"{BASE_URL}/task/claim"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    
    payload = {
        'task_id': TASK_ID,
        'node_id': NODE_ID
    }
    
    print(f"\n发送领取请求...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    print(f"\nHTTP 状态码：{response.status_code}")
    
    try:
        result = response.json()
        print(f"\n响应内容:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 分析响应
        print("\n" + "="*80)
        print("领取结果分析")
        print("="*80)
        
        if response.status_code == 200:
            if result.get('success') or result.get('status') == 'claimed':
                print(f"\n✅ 任务领取成功！")
                print(f"   任务 ID: {TASK_ID}")
                print(f"   赏金：{BOUNTY_AMOUNT} 积分")
                print(f"\n下一步:")
                print(f"1. 开始完成任务")
                print(f"2. 完成后提交结果")
                return True, result
            else:
                print(f"\n⚠️  任务可能已被领取")
                print(f"   状态：{result.get('status', 'unknown')}")
                return False, result
        elif response.status_code == 409:
            print(f"\n⚠️  HTTP 409 冲突")
            print(f"   任务可能已被其他节点领取")
            return False, result
        elif response.status_code == 403:
            print(f"\n❌ HTTP 403 禁止")
            print(f"   原因：{result.get('error', 'unknown')}")
            return False, result
        elif response.status_code == 429:
            print(f"\n⚠️  HTTP 429 限流")
            retry_after = response.headers.get('Retry-After', '30')
            print(f"   等待 {retry_after} 秒后重试")
            return False, result
        else:
            print(f"\n❌ HTTP {response.status_code} 错误")
            print(f"   错误：{result.get('error', 'unknown')}")
            return False, result
            
    except Exception as e:
        print(f"\n❌ 解析响应失败：{e}")
        print(f"原始响应：{response.text[:500]}")
        return False, None

def print_task_details():
    """打印任务详情"""
    print("\n" + "="*80)
    print("任务详情")
    print("="*80)
    
    print(f"""
任务：AI NPC 对话系统硬件指南

需求：
- 为 AI NPC 对话系统（带动态性格）推荐硬件配置
- 包含预算级、中端、专业级三个档次
- 提供具体的硬件型号和设置建议

交付物：
- 详细的硬件配置清单
- 每个档次的价格范围
- 性能对比和推荐理由
- 实施步骤和优化建议

信号标签：
- game-generation
- gamedev
- ai-games
- dialogue systems
- dynamic personality
- hardware guide

预计工作量：2-3 小时
预计收益：493 积分
""")

# 主程序
print("="*80)
print("EvoMap 任务领取")
print("="*80)
print(f"节点：{NODE_ID}")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 打印任务详情
print_task_details()

# 领取任务
print(f"\n[1/2] 领取任务...")
success, result = claim_task()

if success:
    print(f"\n[2/2] 任务已领取，开始执行...")
    print(f"\n" + "="*80)
    print("下一步行动")
    print("="*80)
    print(f"""
1. 研究 AI NPC 对话系统的硬件需求
2. 收集预算级、中端、专业级配置信息
3. 编写详细的硬件指南
4. 提交结果到 EvoMap

预计完成时间：2-3 小时
预计收益：493 积分
完成后积分：493 积分（距离 Premium 还差 1507 积分）
""")
else:
    print(f"\n[2/2] 任务领取失败，选择其他任务...")
    print(f"\n建议:")
    print(f"1. 选择第 2 个任务（3D 工具对比，459 积分）")
    print(f"2. 或选择第 3 个任务（病毒视频质量，391 积分）")

print(f"\n{'='*80}")
