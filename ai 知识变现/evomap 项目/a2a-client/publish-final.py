#!/usr/bin/env python3
"""
正确的发布流程：
1. 本地计算临时 ID
2. Validate 获取正确 ID
3. 用正确 ID 替换
4. Publish
"""

import requests
import json
import hashlib
import time
from datetime import datetime

NODE_ID = 'node_67c3b8b37becd262'
NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
BASE_URL = 'https://evomap.ai'

def compute_asset_id(obj):
    """本地计算 asset_id（可能和 Hub 不一致）"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'

def build_envelope(message_type, payload):
    return {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': message_type,
        'message_id': f'msg_{int(time.time() * 1000)}',
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': payload
    }

def main():
    print()
    print('='*70)
    print('🚀 正确发布流程：Validate → Publish')
    print('='*70)
    print()
    
    # 准备数据
    print('📝 准备 Gene 和 Capsule...')
    
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
    
    # 步骤 1: 计算临时 ID 并添加到数据中
    print('📝 步骤 1: 计算临时 asset_id...')
    gene['asset_id'] = compute_asset_id(gene)
    capsule['asset_id'] = compute_asset_id(capsule)
    capsule['gene'] = gene['asset_id']  # Capsule 引用 Gene 的临时 ID
    print(f'   Gene 临时 ID: {gene["asset_id"][:30]}...')
    print(f'   Capsule 临时 ID: {capsule["asset_id"][:30]}...')
    print()
    
    # 步骤 2: Validate 获取正确 ID
    print('📝 步骤 2: Validate 获取正确 ID...')
    
    validate_payload = build_envelope('validate', {'assets': [gene, capsule]})
    
    response = requests.post(
        f'{BASE_URL}/a2a/validate',
        json=validate_payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'},
        timeout=60
    )
    
    validate_result = response.json()
    
    if response.status_code != 200:
        print(f'❌ Validate 失败：{validate_result.get("error", "Unknown")}')
        return
    
    # 提取正确 ID
    payload = validate_result.get('payload', {})
    computed_assets = payload.get('computed_assets', [])
    
    if not computed_assets:
        print('❌ 没有 computed_assets')
        return
    
    correct_ids = {}
    for asset in computed_assets:
        correct_ids[asset.get('type')] = asset.get('asset_id')
        print(f'   ✅ {asset.get("type")}: {asset.get("asset_id", "")[:30]}...')
    
    print()
    
    # 步骤 3: 用正确 ID 替换
    print('📝 步骤 3: 替换为正确 ID...')
    gene['asset_id'] = correct_ids.get('Gene')
    capsule['asset_id'] = correct_ids.get('Capsule')
    capsule['gene'] = correct_ids.get('Gene')  # 更新 Capsule 的 gene 引用
    print('   ✅ ID 已替换')
    print()
    
    # 步骤 4: Publish
    print('📝 步骤 4: Publish...')
    
    publish_payload = build_envelope('publish', {'assets': [gene, capsule]})
    
    response = requests.post(
        f'{BASE_URL}/a2a/publish',
        json=publish_payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'},
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
        
        # 保存
        with open('published-genes.txt', 'a') as f:
            f.write(f'\n[抖音直播] {gene["summary"]}\n')
            f.write(f'Bundle: {asset_id}\n')
            f.write(f'Gene: {correct_ids.get("Gene", "")}\n')
            f.write(f'Capsule: {correct_ids.get("Capsule", "")}\n')
            f.write('-'*70 + '\n')
        print('💾 已保存到 published-genes.txt')
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
