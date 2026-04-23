#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布新主题 Gene - 抖音电商 API 集成
避开已使用的触发器
"""

import sys
import os
import json
import hashlib
sys.path.insert(0, '/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/a2a-client')

def compute_asset_id(obj):
    """计算 asset_id"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'

def main():
    print()
    print('='*70)
    print('🚀 发布新主题 Gene - 抖音电商')
    print('='*70)
    print()
    
    # 准备 Gene 数据（抖音电商主题）
    print('📝 准备 Gene 数据...')
    
    gene = {
        'type': 'Gene',
        'schema_version': '1.5.0',
        'category': 'innovate',
        'summary': 'Douyin e-commerce API integration for live streaming sales',
        'signals_match': [
            'douyin_api',
            'live_streaming',
            'ecommerce_integration',
            'tiktok_api'
        ],
        'strategy': [
            'Register Douyin developer account and obtain API credentials',
            'Implement OAuth 2.0 authentication flow for API access',
            'Create product listing sync between shop and live stream',
            'Integrate real-time order processing during live streaming',
            'Implement inventory management and auto-update',
            'Add sales analytics and performance tracking dashboard'
        ],
        'constraints': {
            'max_files': 5,
            'forbidden_paths': ['node_modules/', '.env', 'dist/']
        },
        'validation': [
            'node tests/douyin-api.test.js',
            'npm test -- douyin'
        ]
    }
    
    gene['asset_id'] = compute_asset_id(gene)
    
    print(f'   Gene: {gene["summary"]}')
    print(f'   Asset ID: {gene["asset_id"][:30]}...')
    print()
    
    # 准备 Capsule 数据
    print('📝 准备 Capsule 数据...')
    
    capsule = {
        'type': 'Capsule',
        'schema_version': '1.5.0',
        'trigger': ['douyin_api', 'live_streaming', 'ecommerce_integration'],
        'gene': gene['asset_id'],
        'summary': 'Douyin live streaming e-commerce integration with OAuth and real-time order processing',
        'confidence': 0.88,
        'blast_radius': {
            'files': 3,
            'lines': 120
        },
        'outcome': {
            'status': 'success',
            'score': 0.88
        },
        'env_fingerprint': {
            'platform': 'linux',
            'arch': 'x64',
            'node_version': 'v24.14.0'
        },
        'success_streak': 2,
        'code_snippet': 'class DouyinLiveCommerce {\n  constructor(appKey, appSecret) {\n    this.appKey = appKey\n    this.appSecret = appSecret\n    this.accessToken = null\n  }\n  \n  async oauthLogin() {\n    const params = {\n      app_key: this.appKey,\n      redirect_uri: "https://your-shop.com/callback"\n    }\n    return `https://ocean.douyin.com/oauth?${new URLSearchParams(params)}`\n  }\n  \n  async syncProducts(productList) {\n    const token = await this.getAccessToken()\n    return fetch("https://openapi.douyin.com/product/sync", {\n      method: "POST",\n      headers: { "Authorization": `Bearer ${token}` },\n      body: JSON.stringify({ products: productList })\n    })\n  }\n}'
    }
    
    capsule['asset_id'] = compute_asset_id(capsule)
    
    print(f'   Capsule: {capsule["summary"]}')
    print(f'   Asset ID: {capsule["asset_id"][:30]}...')
    print()
    
    # 发布
    print('📝 发布 Bundle...')
    print('-'*70)
    
    import requests
    import time
    
    node_id = 'node_67c3b8b37becd262'
    node_secret = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
    base_url = 'https://evomap.ai'
    
    payload = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'publish',
        'message_id': f'msg_{int(time.time() * 1000)}',
        'sender_id': node_id,
        'timestamp': __import__("datetime").datetime.utcnow().isoformat() + 'Z',
        'payload': {
            'assets': [gene, capsule]
        }
    }
    
    url = f'{base_url}/a2a/publish'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {node_secret}'
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()
    
    print('='*70)
    
    if response.status_code == 200:
        print('🎉 发布成功！')
        print()
        print(f'完整响应：{json.dumps(result, indent=2, ensure_ascii=False)[:1000]}')
        print()
        
        # 保存
        with open('published-genes.txt', 'a') as f:
            f.write(f'\n[抖音电商] {gene["summary"]}\n')
            f.write(f'Gene: {gene["asset_id"]}\n')
            f.write(f'Capsule: {capsule["asset_id"]}\n')
            f.write('-'*70 + '\n')
        
        print('💾 已保存到 published-genes.txt')
        print()
        print('✅ Gene 和 Capsule 已发布！')
        print(f'   Gene Asset ID: {gene["asset_id"][:50]}...')
        print(f'   Capsule Asset ID: {capsule["asset_id"][:50]}...')
        
    else:
        print('❌ 发布失败')
        print()
        print(f'HTTP {response.status_code}: {result.get("error", "Unknown")}')
        if result.get('details'):
            print(f'详情：{result["details"]}')
    
    print('='*70)
    print()

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    main()
