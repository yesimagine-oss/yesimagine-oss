#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询节点已发布资产（带重试）
"""

import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

def query_published_assets(node_id, node_secret, max_retries=5):
    """查询已发布资产"""
    client = GAPA2AClient(node_id, node_secret)
    
    # 先认证
    hello_result = client.hello()
    if not hello_result.get('success'):
        return {'success': False, 'error': hello_result.get('error')}
    
    print(f"✅ 认证成功")
    print(f"  积分余额：{hello_result.get('data', {}).get('payload', {}).get('credit_balance')}")
    print(f"  声誉等级：Level {hello_result.get('data', {}).get('payload', {}).get('capability_profile', {}).get('level')}")
    
    # 尝试查询已发布资产
    # 注意：EvoMap API 可能没有直接的"查询我的资产"端点
    # 我们尝试几个可能的端点
    
    endpoints_to_try = [
        '/a2a/user/assets',
        '/api/user/assets',
        '/a2a/assets?node_id=' + node_id,
    ]
    
    for endpoint in endpoints_to_try:
        print(f"\n尝试端点：{endpoint}")
        
        for attempt in range(max_retries):
            try:
                url = f"{client.base_url}{endpoint}"
                headers = {
                    'Authorization': f'Bearer {node_secret}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 成功！")
                    return {'success': True, 'data': result, 'endpoint': endpoint}
                elif response.status_code == 429:
                    retry_after = response.headers.get('Retry-After', '3')
                    print(f"  ⚠️  限流 (HTTP 429)，等待 {retry_after}秒...")
                    time.sleep(int(retry_after) + 1)
                elif response.status_code == 404:
                    print(f"  ⚠️  端点不存在 (HTTP 404)")
                    break
                else:
                    print(f"  ⚠️  HTTP {response.status_code}: {response.text[:200]}")
                    break
                    
            except Exception as e:
                print(f"  ❌ 错误：{e}")
                if attempt < max_retries - 1:
                    time.sleep(3)
    
    return {'success': False, 'error': '无法查询已发布资产'}

# 2 个节点
nodes = [
    {'name': '新节点（主用）', 'node_id': 'node_cdd0bc78f3a6d99b', 'node_secret': '9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711'},
    {'name': '旧节点（已恢复）', 'node_id': 'node_67c3b8b37becd262', 'node_secret': '8cad4ac975ba7408b9c96f66c2dcfd3e2cd6479e84519a976b111f459858ef86'}
]

print("="*80)
print("查询 2 个节点的已发布资产")
print("="*80)
print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

for node in nodes:
    print(f"\n{'='*80}")
    print(f"节点：{node['name']}")
    print(f"ID: {node['node_id']}")
    print(f"{'='*80}")
    
    result = query_published_assets(node['node_id'], node['node_secret'])
    
    if result.get('success'):
        print(f"\n✅ 查询成功！")
        print(json.dumps(result.get('data'), indent=2, ensure_ascii=False)[:2000])
    else:
        print(f"\n❌ 查询失败：{result.get('error')}")

print(f"\n结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
