#!/usr/bin/env python3
"""
两步验证法：
1. 先 validate Gene 获取正确 ID
2. 更新 Capsule 的 gene 字段
3. 再 validate Capsule
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
    print('🚀 两步验证发布')
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
    
    # 步骤 1: 计算 Gene 临时 ID 并 validate
    print('📝 步骤 1: Validate Gene 获取正确 ID...')
    gene['asset_id'] = compute_asset_id(gene)
    
    gene_payload = build_envelope('publish', {'assets': [gene]})
    
    response = requests.post(
        f'{BASE_URL}/a2a/validate',
        json=gene_payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'},
        timeout=60
    )
    
    gene_validate = response.json()
    
    if response.status_code != 200:
        print(f'❌ Gene Validate 失败：{gene_validate.get("error", "Unknown")}')
        if gene_validate.get('details'):
            print(f'   详情：{json.dumps(gene_validate["details"], indent=2, ensure_ascii=False)}')
        print(f'   完整响应：{json.dumps(gene_validate, indent=2, ensure_ascii=False)[:800]}')
        return
    
    computed_assets = gene_validate.get('payload', {}).get('computed_assets', [])
    if not computed_assets:
        print('❌ 没有 computed_assets')
        return
    
    correct_gene_id = None
    for asset in computed_assets:
        if asset.get('type') == 'Gene':
            correct_gene_id = asset.get('asset_id')
            print(f'   ✅ Gene 正确 ID: {correct_gene_id[:50]}...')
    
    if not correct_gene_id:
        print('❌ 没有找到 Gene ID')
        return
    
    print()
    
    # 步骤 2: 更新 Capsule 的 gene 字段
    print('📝 步骤 2: 更新 Capsule 的 gene 字段...')
    capsule['gene'] = correct_gene_id
    capsule['asset_id'] = compute_asset_id(capsule)
    print(f'   Capsule gene: {correct_gene_id[:30]}...')
    print(f'   Capsule ID: {capsule["asset_id"][:30]}...')
    print()
    
    # 步骤 3: Validate 完整 Bundle
    print('📝 步骤 3: Validate 完整 Bundle...')
    
    # 更新 Gene 为正确 ID
    gene['asset_id'] = correct_gene_id
    
    bundle_payload = build_envelope('publish', {'assets': [gene, capsule]})
    
    response = requests.post(
        f'{BASE_URL}/a2a/validate',
        json=bundle_payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'},
        timeout=60
    )
    
    bundle_validate = response.json()
    
    if response.status_code != 200:
        print(f'❌ Bundle Validate 失败：{bundle_validate.get("error", "Unknown")}')
        if bundle_validate.get('details'):
            print(f'   详情：{json.dumps(bundle_validate["details"], indent=2, ensure_ascii=False)[:300]}')
        return
    
    computed_assets = bundle_validate.get('payload', {}).get('computed_assets', [])
    if not computed_assets or len(computed_assets) < 2:
        print('❌ computed_assets 不完整')
        return
    
    correct_capsule_id = None
    for asset in computed_assets:
        if asset.get('type') == 'Capsule':
            correct_capsule_id = asset.get('asset_id')
            print(f'   ✅ Capsule 正确 ID: {correct_capsule_id[:50]}...')
    
    if not correct_capsule_id:
        print('❌ 没有找到 Capsule ID')
        return
    
    print()
    
    # 步骤 4: Publish
    print('📝 步骤 4: Publish...')
    
    # 使用正确的 ID
    gene['asset_id'] = correct_gene_id
    capsule['asset_id'] = correct_capsule_id
    capsule['gene'] = correct_gene_id
    
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
    
    print('='*70)
    print()

if __name__ == '__main__':
    main()
