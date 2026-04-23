#!/usr/bin/env python3
"""
调试验证错误
"""
import json
import hashlib
import sys
from pathlib import Path
import time
import random
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

def canonicalize(obj):
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        if not (obj == obj):
            return 'null'
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=True)
    if isinstance(obj, list):
        items = [canonicalize(item) for item in obj]
        return '[' + ','.join(items) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = []
        for k in keys:
            key_str = json.dumps(k, ensure_ascii=True)
            val_str = canonicalize(obj[k])
            pairs.append(f'{key_str}:{val_str}')
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj, exclude_fields=None):
    if exclude_fields is None:
        exclude_fields = ['asset_id']
    if not isinstance(obj, dict):
        return None
    clean = {k: v for k, v in obj.items() if k not in exclude_fields}
    canonical = canonicalize(clean)
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return f'sha256:{hash_hex}'

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
client.hello()

# 测试第一个 Bundle
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

assets = []
gene_id = None

for filename, asset_type in [('gene.json', 'Gene'), ('capsule.json', 'Capsule'), ('event.json', 'EvolutionEvent')]:
    asset_file = asset_dir / filename
    with open(asset_file, 'r', encoding='utf-8') as f:
        asset = json.load(f)
    
    asset['type'] = asset_type
    asset['schema_version'] = '1.6.0'
    
    if asset_type == 'Capsule' and gene_id:
        asset['gene'] = gene_id
    
    asset_id = compute_asset_id(asset)
    asset['asset_id'] = asset_id
    
    if asset_type == 'Gene':
        gene_id = asset_id
    
    assets.append(asset)

# 创建信封
timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
message_id = f"msg_{int(time.time() * 1000)}"

envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": message_id,
    "sender_id": NODE_ID,
    "timestamp": timestamp,
    "payload": {"assets": assets}
}

print("发送 publish 请求...")
result = client._send_request('/a2a/publish', envelope)

print(f"\n结果：{result.get('error', 'Success')}")

if result.get('error'):
    print(f"\n完整响应:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 解析 details
    if result.get('data', {}).get('details'):
        try:
            details = json.loads(result['data']['details'])
            print(f"\n\n解析后的错误:")
            print(json.dumps(details, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"\n解析失败：{e}")
            print(f"原始详情：{result['data']['details'][:1000]}")
