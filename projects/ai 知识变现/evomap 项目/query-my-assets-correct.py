#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确查询并过滤 2 个节点的资产
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

def query_and_filter_assets(node_id, node_secret):
    """查询并过滤出自己的资产"""
    client = GAPA2AClient(node_id, node_secret)
    
    # 认证
    hello_result = client.hello()
    if not hello_result.get('success'):
        return {'success': False, 'error': hello_result.get('error')}
    
    # 查询资产
    url = f"{client.base_url}/a2a/assets?node_id={node_id}"
    headers = {
        'Authorization': f'Bearer {node_secret}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        return {'success': False, 'error': f'HTTP {response.status_code}'}
    
    result = response.json()
    all_assets = result.get('assets', [])
    
    # 过滤出自己的资产
    my_assets = [
        asset for asset in all_assets
        if asset.get('source_node_id') == node_id
    ]
    
    # 统计状态
    status_count = {}
    for asset in my_assets:
        status = asset.get('status', 'unknown')
        status_count[status] = status_count.get(status, 0) + 1
    
    return {
        'success': True,
        'total_assets': len(all_assets),
        'my_assets': len(my_assets),
        'status_breakdown': status_count,
        'assets': my_assets
    }

# 2 个节点
nodes = [
    {'name': '新节点（主用）', 'node_id': 'node_cdd0bc78f3a6d99b', 'node_secret': '9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711'},
    {'name': '旧节点（已恢复）', 'node_id': 'node_67c3b8b37becd262', 'node_secret': '8cad4ac975ba7408b9c96f66c2dcfd3e2cd6479e84519a976b111f459858ef86'}
]

print("="*80)
print("正确查询 2 个节点的资产（过滤 source_node_id）")
print("="*80)
print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

for node in nodes:
    print(f"\n{'='*80}")
    print(f"节点：{node['name']}")
    print(f"ID: {node['node_id']}")
    print(f"{'='*80}")
    
    result = query_and_filter_assets(node['node_id'], node['node_secret'])
    
    if result.get('success'):
        print(f"\n✅ 查询成功！")
        print(f"  API 返回总资产：{result['total_assets']} 个")
        print(f"  我的资产（过滤后）：{result['my_assets']} 个")
        print(f"\n  状态分布：")
        for status, count in result['status_breakdown'].items():
            print(f"    {status}: {count} 个")
        
        # 显示前 5 个资产详情
        print(f"\n  资产列表（前 5 个）：")
        for i, asset in enumerate(result['assets'][:5]):
            print(f"    {i+1}. {asset.get('short_title', '无标题')}")
            print(f"       类型：{asset.get('asset_type')} | 状态：{asset.get('status')} | GDI: {asset.get('gdi_score', 'N/A')}")
            print(f"       创建：{asset.get('created_at', 'N/A')}")
    else:
        print(f"\n❌ 查询失败：{result.get('error')}")

print(f"\n结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
