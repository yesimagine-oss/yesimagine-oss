#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用现有资产包测试发布（带 asset_id）
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"

def canonicalize(obj):
    """生成 canonical JSON 字符串"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonicalize(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj):
    """计算 asset_id: sha256(canonical_json(asset_without_asset_id))"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'

# 加载现有资产包
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

with open(asset_dir / 'gene.json', 'r', encoding='utf-8') as f:
    gene = json.load(f)

with open(asset_dir / 'capsule.json', 'r', encoding='utf-8') as f:
    capsule = json.load(f)

with open(asset_dir / 'event.json', 'r', encoding='utf-8') as f:
    event = json.load(f)

# 计算并添加 asset_id
print("计算 asset_id...")
gene['asset_id'] = compute_asset_id(gene)
print(f"Gene: {gene['asset_id'][:60]}...")

capsule['gene'] = gene['asset_id']  # 更新 gene 引用
capsule['asset_id'] = compute_asset_id(capsule)
print(f"Capsule: {capsule['asset_id'][:60]}...")

event['capsule_id'] = capsule['asset_id']  # 更新 capsule 引用
event['genes_used'] = [gene['asset_id']]  # 更新 gene 引用
event['asset_id'] = compute_asset_id(event)
print(f"Event: {event['asset_id'][:60]}...")

# 构建发布请求
req = {
    'protocol': 'gep-a2a',
    'protocol_version': '1.0.0',
    'message_type': 'publish',
    'message_id': f'msg_{int(datetime.utcnow().timestamp()*1000)}',
    'sender_id': NODE_ID,
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'payload': {
        'assets': [gene, capsule, event]
    }
}

print("\n发送发布请求...")

client = GAPA2AClient(NODE_ID, NODE_SECRET)
client.hello()

result = client._send_request('/a2a/publish', req)

print("\n" + "="*60)
print("响应结果")
print("="*60)

if result.get('error'):
    print(f"❌ 错误：{result.get('error')}")
    print(f"\n详细信息:")
    if result.get('data', {}).get('details'):
        try:
            details = json.loads(result['data']['details'])
            print(json.dumps(details, indent=2, ensure_ascii=False))
        except:
            print(result['data']['details'][:1000])
else:
    print(f"✅ 发布成功！")
    published = result.get('payload', {}).get('published_assets', [])
    print(f"   发布资产数：{len(published)}")
    for asset in published:
        print(f"   - {asset.get('type')}: {asset.get('asset_id', '')[:60]}...")
    print(f"\n完整响应:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
