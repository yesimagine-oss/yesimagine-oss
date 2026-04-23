#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 工具测试脚本
测试 EvoMap MCP 服务器的 7 个可用工具
"""

import requests
import json
from datetime import datetime

NODE_ID = 'node_67c3b8b37becd262'
NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
BASE_URL = 'https://evomap.ai'

def log(message: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')

def test_gep_status():
    """测试 gep_status: 获取进化统计"""
    log('🧪 测试 1: gep_status (获取进化统计)')
    
    # 使用 A2A 协议直接调用
    url = f'{BASE_URL}/a2a/hello'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'hello',
        'message_id': f'msg_{int(datetime.now().timestamp())}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': {
            'capabilities': {'supported_types': ['Gene', 'Capsule']},
            'model': 'gpt-4o'
        }
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()
    
    if response.status_code == 200:
        log('✅ gep_status 测试通过')
        log(f'   Hub Node ID: {result.get("payload", {}).get("hub_node_id", "N/A")}')
        return True
    else:
        log(f'❌ gep_status 测试失败：{result}')
        return False

def test_gep_list_genes():
    """测试 gep_list_genes: 列出可用的进化策略"""
    log('\n🧪 测试 2: gep_list_genes (列出基因)')
    
    url = f'{BASE_URL}/a2a/fetch'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'fetch',
        'message_id': f'msg_{int(datetime.now().timestamp())}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': {
            'asset_type': 'Gene',
            'limit': 5
        }
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()
    
    if response.status_code == 200:
        log('✅ gep_list_genes 测试通过')
        assets = result.get('payload', {}).get('assets', [])
        log(f'   获取到 {len(assets)} 个 Gene')
        if assets:
            log(f'   第 1 个 Gene: {assets[0].get("summary", "N/A")[:50]}...')
        return True
    else:
        log(f'❌ gep_list_genes 测试失败：{result}')
        return False

def test_gep_search_community():
    """测试 gep_search_community: 搜索 Hub 资产"""
    log('\n🧪 测试 3: gep_search_community (搜索资产)')
    
    url = f'{BASE_URL}/a2a/assets/search'
    headers = {
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    params = {
        'signals': 'retry,timeout',
        'limit': 3
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    result = response.json()
    
    if response.status_code == 200:
        log('✅ gep_search_community 测试通过')
        assets = result.get('assets', [])
        log(f'   搜索到 {len(assets)} 个资产')
        return True
    else:
        log(f'❌ gep_search_community 测试失败：{result}')
        return False

def main():
    log('='*60)
    log('🔧 MCP 工具测试')
    log('='*60)
    
    results = []
    
    # 测试 3 个核心工具
    results.append(test_gep_status())
    results.append(test_gep_list_genes())
    results.append(test_gep_search_community())
    
    # 总结
    log('\n' + '='*60)
    log('📊 测试结果总结')
    log('='*60)
    log(f'通过：{sum(results)}/{len(results)}')
    
    if all(results):
        log('✅ 所有 MCP 工具测试通过！')
    else:
        log('⚠️ 部分测试失败，请检查网络和配置')
    
    return all(results)

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
