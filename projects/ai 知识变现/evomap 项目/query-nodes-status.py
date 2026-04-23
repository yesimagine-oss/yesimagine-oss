#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询 2 个节点的发布状态
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

# 2 个节点配置
nodes = [
    {
        'name': '新节点（主用）',
        'node_id': 'node_cdd0bc78f3a6d99b',
        'node_secret': '9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711'
    },
    {
        'name': '旧节点（已恢复）',
        'node_id': 'node_67c3b8b37becd262',
        'node_secret': '8cad4ac975ba7408b9c96f66c2dcfd3e2cd6479e84519a976b111f459858ef86'
    }
]

print("="*80)
print("查询 2 个节点的发布状态")
print("="*80)

for node in nodes:
    print(f"\n{'='*80}")
    print(f"节点：{node['name']}")
    print(f"ID: {node['node_id']}")
    print(f"{'='*80}")
    
    client = GAPA2AClient(node['node_id'], node['node_secret'])
    result = client.hello()
    
    if result.get('success'):
        payload = result.get('data', {}).get('payload', {})
        print(f"✅ 认证成功")
        print(f"  Hub Node ID: {payload.get('hub_node_id')}")
        print(f"  Owner User ID: {payload.get('owner_user_id')}")
        print(f"  积分余额：{payload.get('credit_balance')}")
        print(f"  状态：{payload.get('status')}")
        print(f"  声誉等级：Level {payload.get('capability_profile', {}).get('level')}")
        print(f"  声誉值：{payload.get('capability_profile', {}).get('reputation')}")
    else:
        print(f"❌ 认证失败：{result.get('error')}")

print("\n" + "="*80)
print("注意：由于平台限流（HTTP 429），无法查询已发布资产列表")
print("需要调用 /a2a/user/assets 或类似端点，但当前被限流")
print("="*80)
