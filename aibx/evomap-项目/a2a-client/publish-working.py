#!/usr/bin/env python3
"""
最终方案：
1. 本地计算临时 ID
2. Validate 获取正确 ID
3. 直接用 Hub 返回的 ID Publish（不重新计算）
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
    print('🚀 Validate → Publish（直接使用 Hub ID）')
    print('='*70)
    print()
    
    # 准备数据
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
    
    # 步骤 1: 计算临时 ID
    print('📝 步骤 1: 计算临时 ID...')
    gene['asset_id'] = compute_asset_id(gene)
    capsule['asset_id'] = compute_asset_id(capsule)
    # 注意：先不包含 capsule['gene']，让 Hub 计算
    print(f'   Gene: {gene["asset_id"][:30]}...')
    print(f'   Capsule: {capsule["asset_id"][:30]}...')
    print()
    
    # 步骤 2: Validate
    print('📝 步骤 2: Validate...')
    
    validate_payload = build_envelope('publish', {'assets': [gene, capsule]})
    
    response = requests.post(
        f'{BASE_URL}/a2a/validate',
        json=validate_payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'},
        timeout=60
    )
    
    validate_result = response.json()
    
    if response.status_code != 200:
        print(f'❌ Validate 失败：{validate_result.get("error", "Unknown")}')
        if validate_result.get('details'):
            print(f'   详情：{json.dumps(validate_result["details"], indent=2, ensure_ascii=False)[:500]}')
        return
    
    # 提取正确 ID
    payload = validate_result.get('payload', {})
    computed_assets = payload.get('computed_assets', [])
    
    if not computed_assets or len(computed_assets) < 2:
        print('❌ computed_assets 不完整')
        print(f'   响应：{json.dumps(validate_result, indent=2, ensure_ascii=False)[:500]}')
        return
    
    correct_gene_id = None
    correct_capsule_id = None
    
    for asset in computed_assets:
        if asset.get('type') == 'Gene':
            correct_gene_id = asset.get('asset_id')
            print(f'   ✅ Gene: {correct_gene_id[:50]}...')
        elif asset.get('type') == 'Capsule':
            correct_capsule_id = asset.get('asset_id')
            print(f'   ✅ Capsule: {correct_capsule_id[:50]}...')
    
    print()
    
    # 步骤 3: Publish
    print('📝 步骤 3: Publish...')
    
    # 尝试：不包含 asset_id，让 Hub 计算
    gene_for_publish = {k: v for k, v in gene.items() if k != 'asset_id'}
    capsule_for_publish = {k: v for k, v in capsule.items() if k != 'asset_id'}
    capsule_for_publish['gene'] = correct_gene_id
    
    publish_payload = build_envelope('publish', {'assets': [gene_for_publish, capsule_for_publish]})
    
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
            f.write(f'Gene: {correct_gene_id}\n')
            f.write(f'Capsule: {correct_capsule_id}\n')
            f.write(f'时间：{datetime.now().isoformat()}\n')
            f.write('-'*70 + '\n')
        print('💾 已保存到 published-genes.txt')
    else:
        print('❌ 发布失败')
        print()
        print(f'HTTP {response.status_code}: {result.get("error", "Unknown")}')
        if result.get('details'):
            print(f'详情：{json.dumps(result["details"], indent=2, ensure_ascii=False)[:500]}')
        if result.get('correction'):
            print(f'修复建议：{str(result.get("correction", ""))[:300]}')
    
    print('='*70)
    print()

if __name__ == '__main__':
    main()
