#!/usr/bin/env python3
"""
重试发布
"""
import json
import hashlib
import sys
import time
import random
from pathlib import Path
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
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=True)
    if isinstance(obj, list):
        return '[' + ','.join([canonicalize(item) for item in obj]) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=True)}:{canonicalize(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj):
    if not isinstance(obj, dict):
        return None
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    return f'sha256:{hashlib.sha256(canonical.encode("utf-8")).hexdigest()}'

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
client.hello()

asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

assets = []
gene_id = None

for filename, asset_type in [('gene.json', 'Gene'), ('capsule.json', 'Capsule'), ('event.json', 'EvolutionEvent')]:
    with open(asset_dir / filename, 'r', encoding='utf-8') as f:
        asset = json.load(f)
    
    asset['type'] = asset_type
    asset['schema_version'] = '1.6.0'
    
    if asset_type == 'Capsule' and gene_id:
        asset['gene'] = gene_id
    
    asset['asset_id'] = compute_asset_id(asset)
    
    if asset_type == 'Gene':
        gene_id = asset['asset_id']
    
    assets.append(asset)
    print(f"{asset_type}: {asset['asset_id'][:60]}...")

# 重试逻辑
max_retries = 5
for attempt in range(max_retries):
    print(f"\n🔄 尝试 {attempt + 1}/{max_retries}...")
    
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
    envelope = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": f"msg_{int(time.time() * 1000)}",
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {"assets": assets}
    }
    
    result = client._send_request('/a2a/publish', envelope)
    
    if result.get('error'):
        error = result.get('error', 'Unknown')
        print(f"❌ {error}")
        
        if '503' in str(error) or 'server_busy' in str(result):
            retry_after = result.get('data', {}).get('retry_after_ms', 3000)
            print(f"⏳ 等待 {retry_after}ms...")
            time.sleep(retry_after / 1000 + 2)
        elif '400' in str(error):
            print(f"\n详细错误:")
            if result.get('data', {}).get('details'):
                try:
                    details = json.loads(result['data']['details'])
                    print(json.dumps(details, indent=2, ensure_ascii=False)[:1000])
                except:
                    print(result['data']['details'][:500])
            break
    else:
        print(f"\n✅ 发布成功！")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
        break
else:
    print(f"\n❌ 达到最大重试次数，建议手动发布")
