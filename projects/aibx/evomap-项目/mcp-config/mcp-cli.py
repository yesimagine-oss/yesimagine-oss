#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 工具命令行调用脚本
适用于服务器环境，无需桌面应用
"""

import requests
import json
from datetime import datetime

NODE_ID = 'node_67c3b8b37becd262'
NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
BASE_URL = 'https://evomap.ai'

def log(message: str, emoji: str = '📝'):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f'[{timestamp}] {emoji} {message}')

def gep_status():
    """获取进化统计"""
    log('调用 gep_status (获取进化统计)', '📊')
    
    url = f'{BASE_URL}/a2a/hello'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'}
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'hello',
        'message_id': f'msg_{int(datetime.now().timestamp())}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': {'capabilities': {'supported_types': ['Gene', 'Capsule']}, 'model': 'gpt-4o'}
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()
    
    if response.status_code == 200:
        hub_node_id = result.get('payload', {}).get('hub_node_id', 'N/A')
        log(f'✅ Hub Node ID: {hub_node_id}', '✅')
        return result
    else:
        log(f'❌ 失败：{result}', '❌')
        return None

def gep_list_genes(limit: int = 5):
    """列出可用的进化策略"""
    log(f'调用 gep_list_genes (列出基因，limit={limit})', '🧬')
    
    url = f'{BASE_URL}/a2a/fetch'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'}
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'fetch',
        'message_id': f'msg_{int(datetime.now().timestamp())}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': {'asset_type': 'Gene', 'limit': limit}
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()
    
    if response.status_code == 200:
        assets = result.get('payload', {}).get('assets', [])
        log(f'✅ 获取到 {len(assets)} 个 Gene', '✅')
        for i, asset in enumerate(assets[:3], 1):
            summary = asset.get('summary', 'N/A')[:50]
            log(f'   {i}. {summary}...', '📄')
        return result
    else:
        log(f'❌ 失败：{result}', '❌')
        return None

def gep_search_assets(signals: str = 'retry,timeout', limit: int = 3):
    """搜索 Hub 资产"""
    log(f'调用 gep_search_assets (搜索：{signals}, limit={limit})', '🔍')
    
    url = f'{BASE_URL}/a2a/assets/search'
    headers = {'Authorization': f'Bearer {NODE_SECRET}'}
    params = {'signals': signals, 'limit': limit}
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    result = response.json()
    
    if response.status_code == 200:
        assets = result.get('assets', [])
        log(f'✅ 搜索到 {len(assets)} 个资产', '✅')
        for i, asset in enumerate(assets, 1):
            title = asset.get('summary', asset.get('title', 'N/A'))[:50]
            log(f'   {i}. {title}...', '📄')
        return result
    else:
        log(f'❌ 失败：{result}', '❌')
        return None

def gep_publish_gene(summary: str, signals: list, strategy: list):
    """发布 Gene"""
    log(f'调用 gep_publish_gene (发布基因)', '📤')
    
    import hashlib
    gene = {
        'type': 'Gene',
        'schema_version': '1.5.0',
        'category': 'repair',
        'signals_match': signals,
        'summary': summary,
        'strategy': strategy,
        'constraints': {'max_files': 5, 'forbidden_paths': ['node_modules/', '.env']},
        'validation': ['node tests/test.js']
    }
    
    # 计算 asset_id
    gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
    canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'))
    gene['asset_id'] = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
    
    url = f'{BASE_URL}/a2a/publish'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'}
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'publish',
        'message_id': f'msg_{int(datetime.now().timestamp())}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': {'assets': [gene]}
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()
    
    if response.status_code == 200:
        asset_id = result.get('payload', {}).get('asset_id', 'N/A')[:20]
        log(f'✅ 发布成功！Asset ID: {asset_id}...', '✅')
        return result
    else:
        log(f'❌ 发布失败：{result}', '❌')
        return None

def main():
    print('='*60)
    print('🔧 MCP 工具命令行调用（服务器环境）')
    print('='*60)
    print()
    
    # 测试 1: gep_status
    gep_status()
    print()
    
    # 测试 2: gep_list_genes
    gep_list_genes(limit=5)
    print()
    
    # 测试 3: gep_search_assets
    gep_search_assets(signals='retry,timeout', limit=3)
    print()
    
    print('='*60)
    print('✅ 所有 MCP 工具调用完成！')
    print('='*60)
    print()
    print('💡 使用提示:')
    print('   python3 mcp-cli.py                    # 运行所有测试')
    print('   python3 mcp-cli.py --status           # 只测试 gep_status')
    print('   python3 mcp-cli.py --list-genes       # 只测试 gep_list_genes')
    print('   python3 mcp-cli.py --search "retry"   # 搜索资产')
    print()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--status':
            gep_status()
        elif sys.argv[1] == '--list-genes':
            gep_list_genes()
        elif sys.argv[1] == '--search':
            query = sys.argv[2] if len(sys.argv) > 2 else 'retry'
            gep_search_assets(signals=query)
        else:
            print(f'未知参数：{sys.argv[1]}')
    else:
        main()
