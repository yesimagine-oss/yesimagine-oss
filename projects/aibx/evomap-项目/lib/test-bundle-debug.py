#!/usr/bin/env python3
import json
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
client.hello()

# 读取所有资产
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

assets = []
gene_id = None

for filename, asset_type in [('gene.json', 'Gene'), ('capsule.json', 'Capsule'), ('event.json', 'EvolutionEvent')]:
    asset_file = asset_dir / filename
    with open(asset_file, 'r', encoding='utf-8') as f:
        asset = json.load(f)
    
    asset['type'] = asset_type
    asset['schema_version'] = '1.6.0'
    
    # Capsule 需要 gene 引用
    if asset_type == 'Capsule' and gene_id:
        asset['gene'] = gene_id
    
    # 计算 asset_id
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    asset_canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    asset_id = f"sha256:{hashlib.sha256(asset_canonical.encode('utf-8')).hexdigest()}"
    asset['asset_id'] = asset_id
    
    if asset_type == 'Gene':
        gene_id = asset_id
    
    assets.append(asset)
    print(f"{asset_type}: {asset_id[:60]}...")

# 创建信封
import time
import random
from datetime import datetime

timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
message_id = f"msg_{int(time.time() * 1000)}"

envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": message_id,
    "sender_id": NODE_ID,
    "timestamp": timestamp,
    "payload": {
        "assets": assets
    }
}

print(f"\n🚀 发布 Bundle...")
result = client._send_request('/a2a/publish', envelope)

print(f"\n完整响应状态码：{result.get('error', 'Success')}")

# 检查是否有 computed_asset_id
if result.get('data', {}).get('details'):
    details = json.loads(result['data']['details'])
    print(f"\n\n详细错误:")
    print(json.dumps(details, indent=2, ensure_ascii=False))
    
    # 查找 computed_asset_id
    correction = details.get('correction', {})
    for key, value in correction.items():
        if 'asset_id' in key.lower() and isinstance(value, str) and value.startswith('sha256:'):
            print(f"\n\n✅ Hub 返回的正确 {key}:")
            print(value)
