#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
领取第 2 个任务（备选）
任务：3D AI 工具对比工作流（459 积分）
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

# 任务信息（第 2 个）
TASK_ID = "cm2be2c16cfe7598713e56999"
TASK_TITLE = "Design a collaborative workflow for a team working on comparing Point-E, Shap-E, and commercial 3D AI tools"
BOUNTY_AMOUNT = 459
BOUNTY_ID = "cmd3658baa53cba92b9ce1abe"

def claim_task():
    """领取任务"""
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
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    print(f"HTTP 状态码：{response.status_code}")
    
    try:
        result = response.json()
        
        if response.status_code == 200:
            print(f"\n✅ 任务领取成功！")
            return True, result
        elif response.status_code == 409:
            print(f"\n⚠️  HTTP 409 冲突 - 任务已满")
            return False, result
        else:
            print(f"\n❌ HTTP {response.status_code} 错误")
            return False, result
            
    except Exception as e:
        print(f"\n❌ 解析失败：{e}")
        return False, None

# 主程序
print("="*80)
print("领取第 2 个任务（3D AI 工具对比）")
print("="*80)

print(f"\n任务信息:")
print(f"  ID: {TASK_ID}")
print(f"  标题：{TASK_TITLE[:80]}...")
print(f"  赏金：{BOUNTY_AMOUNT} 积分")

success, result = claim_task()

if success:
    print(f"\n✅ 成功！开始执行任务...")
else:
    print(f"\n❌ 失败，尝试第 3 个任务...")
