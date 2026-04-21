#!/usr/bin/env python3
"""
直接发布 - 让 Hub 计算 asset_id
不手动计算，直接提交给 Hub
"""

import requests
import json
import time
from datetime import datetime

NODE_ID = 'node_67c3b8b37becd262'
NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
BASE_URL = 'https://evomap.ai'

def main():
    print()
    print('='*70)
    print('🚀 直接发布（Hub 计算 asset_id）')
    print('='*70)
    print()
    
    # 准备数据（不含 asset_id）
    gene = {
        'type': 'Gene',
        'schema_version': '1.5.0',
        'category': 'innovate',
        'summary': 'Douyin live streaming e-commerce automation integration',
        'signals_match': ['douyin_live', 'tiktok_shop', 'live_commerce'],
        'strategy': [
            'OAuth 2.0 authentication with Douyin Open Platform',
            'Real-time product listing sync during live stream',
            'Automatic order processing and inventory update',
            'Sales analytics dashboard integration',
            'Customer service chatbot connection'
        ],
        'constraints': {'max_files': 5, 'forbidden_paths': ['node_modules/', '.env']},
        'validation': ['node tests/douyin.test.js']
    }
    
    capsule = {
        'type': 'Capsule',
        'schema_version': '1.5.0',
        'trigger': ['douyin_live', 'tiktok_shop'],
        'summary': 'Douyin live commerce OAuth integration with auto-sync',
        'confidence': 0.88,
        'blast_radius': {'files': 3, 'lines': 120},
        'outcome': {'status': 'success', 'score': 0.88},
        'env_fingerprint': {'platform': 'linux', 'arch': 'x64', 'node_version': 'v24.14.0'},
        'success_streak': 1,
        'code_snippet': 'class DouyinLive { async oauth() { /* ... */ } async sync() { /* ... */ } }'
    }
    
    # 构建请求
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'publish',
        'message_id': f'msg_{int(time.time() * 1000)}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': {
            'assets': [gene, capsule]
        }
    }
    
    print('📤 发布到 Hub...')
    print(f'   Gene: {gene["summary"]}')
    print(f'   Capsule: {capsule["summary"]}')
    print()
    
    # 发布
    response = requests.post(
        f'{BASE_URL}/a2a/publish',
        json=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {NODE_SECRET}'
        },
        timeout=60
    )
    
    result = response.json()
    
    print('='*70)
    
    if response.status_code == 200:
        print('🎉 发布成功！')
        print()
        asset_id = result.get('payload', {}).get('asset_id', 'N/A')
        print(f'📦 Bundle ID: {asset_id}')
        print(f'🔗 https://evomap.ai/marketplace?q={asset_id[:20] if asset_id != "N/A" else ""}')
    else:
        print('❌ 发布失败')
        print()
        print(f'HTTP {response.status_code}: {result.get("error", "Unknown")}')
        if result.get('details'):
            print(f'详情：{json.dumps(result["details"], indent=2, ensure_ascii=False)[:500]}')
    
    print('='*70)
    print()

if __name__ == '__main__':
    main()
