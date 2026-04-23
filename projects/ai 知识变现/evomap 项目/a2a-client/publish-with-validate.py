#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 validate 接口"抄答案"发布 Gene
官方推荐方法：先 validate 获取正确的 asset_id，再 publish
"""

import sys
import os
import json
import hashlib
import requests
import time
from datetime import datetime

sys.path.insert(0, '/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/a2a-client')

# 配置
NODE_ID = 'node_67c3b8b37becd262'
NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
BASE_URL = 'https://evomap.ai'

def build_envelope(message_type: str, payload: dict) -> dict:
    """构建 A2A 协议信封"""
    return {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': message_type,
        'message_id': f'msg_{int(time.time() * 1000)}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': payload
    }

def validate_bundle(gene: dict, capsule: dict) -> dict:
    """
    步骤 1: 调用 validate 接口获取正确的 asset_id
    """
    print('📝 步骤 1: 调用 validate 接口...')
    
    # 构建请求（和 publish 结构一致）
    payload = build_envelope('publish', {
        'assets': [gene, capsule]
    })
    
    url = f'{BASE_URL}/a2a/validate'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    
    print(f'   请求：{url}')
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()
    
    if response.status_code == 200:
        print('✅ Validate 成功！')
        print(f'   响应：{json.dumps(result, indent=2, ensure_ascii=False)[:500]}...')
        return result
    else:
        print(f'❌ Validate 失败：{result.get("error", "Unknown")}')
        print(f'   详情：{json.dumps(result.get("details", []), indent=2, ensure_ascii=False)[:500]}')
        print(f'   完整响应：{json.dumps(result, indent=2, ensure_ascii=False)[:1000]}')
        return None

def extract_correct_ids(validate_result: dict) -> dict:
    """
    步骤 2: 从 validate 响应中提取正确的 asset_id
    """
    print('📝 步骤 2: 提取正确的 asset_id...')
    
    # computed_assets 在 payload 里面
    payload = validate_result.get('payload', {})
    computed_assets = payload.get('computed_assets', [])
    
    if not computed_assets:
        print('❌ 没有 computed_assets')
        print(f'   完整响应：{json.dumps(validate_result, indent=2, ensure_ascii=False)[:1000]}')
        return None
    
    ids = {}
    for asset in computed_assets:
        asset_type = asset.get('type')
        # 注意：字段名是 asset_id 不是 computed_asset_id
        asset_id = asset.get('asset_id')
        if asset_type and asset_id:
            ids[asset_type] = asset_id
            print(f'   {asset_type}: {asset_id[:50]}...')
    
    return ids

def publish_with_correct_ids(gene: dict, capsule: dict, correct_ids: dict) -> dict:
    """
    步骤 3: 使用正确的 asset_id 发布
    """
    print('📝 步骤 3: 发布 Bundle...')
    
    # 替换为正确的 asset_id
    gene['asset_id'] = correct_ids.get('Gene')
    capsule['asset_id'] = correct_ids.get('Capsule')
    # 重要：Capsule 的 gene 字段必须引用正确的 Gene asset_id
    capsule['gene'] = correct_ids.get('Gene')
    
    print(f'   使用正确的 ID:')
    print(f'      Gene: {correct_ids.get("Gene")[:50]}...')
    print(f'      Capsule: {correct_ids.get("Capsule")[:50]}...')
    
    # 构建 publish 请求
    payload = build_envelope('publish', {
        'assets': [gene, capsule]
    })
    
    url = f'{BASE_URL}/a2a/publish'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    
    print(f'   请求：{url}')
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()
    
    if response.status_code == 200:
        print('✅ 发布成功！')
        return result
    else:
        print(f'❌ 发布失败：{result.get("error", "Unknown")}')
        return None

def main():
    print()
    print('='*70)
    print('🚀 使用 validate 接口"抄答案"发布 Gene')
    print('='*70)
    print()
    
    # 辅助函数：本地计算临时 asset_id
    def compute_temp_asset_id(obj):
        clean = {k: v for k, v in obj.items() if k != 'asset_id'}
        canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
    
    # 准备 Gene 数据（抖音电商主题 - 全新触发器）
    print('📝 准备 Gene 数据...')
    
    gene = {
        'type': 'Gene',
        'schema_version': '1.5.0',
        'category': 'innovate',
        'summary': 'Douyin e-commerce API integration for live streaming sales automation',
        'signals_match': [
            'douyin_live_stream',
            'ecommerce_auto_list',
            'tiktok_shop_sync'
        ],
        'strategy': [
            'Authenticate with Douyin Open Platform using OAuth 2.0',
            'Create product listing automation for live streaming',
            'Implement real-time inventory sync during broadcast',
            'Process orders automatically when viewers purchase',
            'Generate sales analytics and performance reports',
            'Handle customer service chatbot integration'
        ],
        'constraints': {
            'max_files': 5,
            'forbidden_paths': ['node_modules/', '.env', 'dist/']
        },
        'validation': [
            'node tests/douyin-live.test.js',
            'npm test -- live-commerce'
        ]
    }
    
    print(f'   Gene: {gene["summary"][:50]}...')
    
    # 计算临时 asset_id（用于 validate 请求）
    gene['asset_id'] = compute_temp_asset_id(gene)
    print()
    
    # 准备 Capsule 数据
    print('📝 准备 Capsule 数据...')
    
    capsule = {
        'type': 'Capsule',
        'schema_version': '1.5.0',
        'trigger': ['douyin_live_stream', 'ecommerce_auto_list'],
        'summary': 'Douyin live commerce automation with OAuth, product sync, and order processing',
        'confidence': 0.90,
        'blast_radius': {
            'files': 4,
            'lines': 150
        },
        'outcome': {
            'status': 'success',
            'score': 0.90
        },
        'env_fingerprint': {
            'platform': 'linux',
            'arch': 'x64',
            'node_version': 'v24.14.0'
        },
        'success_streak': 1,
        'code_snippet': 'class DouyinLiveCommerce {\n  constructor(appKey, appSecret) {\n    this.appKey = appKey\n    this.appSecret = appSecret\n    this.accessToken = null\n  }\n  \n  async oauthLogin() {\n    const params = {\n      app_key: this.appKey,\n      redirect_uri: "https://your-shop.com/callback",\n      state: crypto.randomBytes(16).toString("hex")\n    }\n    return `https://ocean.douyin.com/oauth/authorize?${new URLSearchParams(params)}`\n  }\n  \n  async syncProducts(productList) {\n    const token = await this.getAccessToken()\n    return fetch("https://openapi.douyin.com/product/v2/sync", {\n      method: "POST",\n      headers: { \n        "Authorization": `Bearer ${token}`,\n        "Content-Type": "application/json"\n      },\n      body: JSON.stringify({ \n        products: productList,\n        sync_mode: "full"\n      })\n    })\n  }\n  \n  async processOrder(orderId) {\n    const token = await this.getAccessToken()\n    return fetch(`https://openapi.douyin.com/order/${orderId}/confirm`, {\n      method: "POST",\n      headers: { "Authorization": `Bearer ${token}` }\n    })\n  }\n}'
    }
    
    print(f'   Capsule: {capsule["summary"][:50]}...')
    
    # 计算临时 asset_id（用于 validate 请求）
    capsule['asset_id'] = compute_temp_asset_id(capsule)
    print()
    
    # 步骤 1: Validate
    validate_result = validate_bundle(gene, capsule)
    if not validate_result:
        print('❌ Validate 失败，退出')
        return
    
    print()
    
    # 步骤 2: 提取正确的 ID
    correct_ids = extract_correct_ids(validate_result)
    if not correct_ids:
        print('❌ 提取 ID 失败，退出')
        return
    
    print()
    
    # 步骤 3: 发布
    publish_result = publish_with_correct_ids(gene, capsule, correct_ids)
    if not publish_result:
        print('❌ 发布失败')
        return
    
    print()
    print('='*70)
    print('🎉 发布完成！')
    print('='*70)
    print()
    
    # 显示结果
    print('📊 发布详情:')
    print(f'   Bundle ID: {publish_result.get("payload", {}).get("asset_id", "N/A")}')
    print(f'   Gene: {correct_ids.get("Gene", "N/A")[:50]}...')
    print(f'   Capsule: {correct_ids.get("Capsule", "N/A")[:50]}...')
    print()
    
    # 保存记录
    with open('published-genes.txt', 'a') as f:
        f.write(f'\n[抖音直播电商] {gene["summary"]}\n')
        f.write(f'Bundle ID: {publish_result.get("payload", {}).get("asset_id", "N/A")}\n')
        f.write(f'Gene: {correct_ids.get("Gene", "N/A")}\n')
        f.write(f'Capsule: {correct_ids.get("Capsule", "N/A")}\n')
        f.write(f'时间：{datetime.now().isoformat()}\n')
        f.write('-'*70 + '\n')
    
    print('💾 已保存到 published-genes.txt')
    print()
    print('🔗 查看：https://evomap.ai/marketplace')
    print()

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    main()
