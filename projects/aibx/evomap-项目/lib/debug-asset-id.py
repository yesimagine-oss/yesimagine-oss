#!/usr/bin/env python3
import json
import sys
import hashlib
import time
import random
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)

def compute_asset_id_canonical(asset: dict) -> str:
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    # 使用 ensure_ascii=False 匹配 JS 的 JSON.stringify
    canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return f"sha256:{hash_hex}"

def create_publish_envelope(assets: list) -> dict:
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
    message_id = f"msg_{int(time.time() * 1000)}_{hashlib.md5(timestamp.encode()).hexdigest()[:8]}"
    return {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {"assets": assets}
    }

# 读取 3 个组件
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")
assets = []

for filename, asset_type in [('gene.json', 'Gene'), ('capsule.json', 'Capsule'), ('event.json', 'EvolutionEvent')]:
    asset_file = asset_dir / filename
    with open(asset_file, 'r', encoding='utf-8') as f:
        asset_data = json.load(f)
    
    asset_data['type'] = asset_type
    # 保持原始 schema_version
    if 'schema_version' not in asset_data:
        asset_data['schema_version'] = '1.6.0'
    asset_id = compute_asset_id_canonical(asset_data)
    asset_data['asset_id'] = asset_id
    assets.append(asset_data)
    
    print(f"{asset_type}: {asset_id[:60]}...")

# 发布
envelope = create_publish_envelope(assets)
result = client._send_request('/a2a/publish', envelope)

print(f"\n\n完整响应:")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 尝试解析 details 查找 computed_asset_id
if result.get('data', {}).get('details'):
    try:
        details = json.loads(result['data']['details'])
        print(f"\n\n解析后的错误详情:")
        print(json.dumps(details, indent=2, ensure_ascii=False))
        
        # 查找 computed_asset_id
        if 'computed_asset_id' in details.get('correction', {}):
            print(f"\n\n✅ Hub 返回的正确 asset_id:")
            print(details['correction']['computed_asset_id'])
    except Exception as e:
        print(f"\n解析 details 失败：{e}")

# 检查是否有 computed_asset_id
if result.get('data', {}).get('details'):
    try:
        details = json.loads(result['data']['details'])
        print(f"\n\n详细错误解析:")
        print(json.dumps(details, indent=2, ensure_ascii=False))
        
        if details.get('correction', {}).get('computed_asset_id'):
            print(f"\n\n✅ Hub 返回的正确 asset_id:")
            print(details['correction']['computed_asset_id'])
    except Exception as e:
        print(f"解析失败：{e}")
