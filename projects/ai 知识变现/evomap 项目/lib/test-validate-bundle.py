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

# 读取所有资产（不包含 asset_id）
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

assets_without_id = []
gene_id = None

for filename, asset_type in [('gene.json', 'Gene'), ('capsule.json', 'Capsule'), ('event.json', 'EvolutionEvent')]:
    asset_file = asset_dir / filename
    with open(asset_file, 'r', encoding='utf-8') as f:
        asset = json.load(f)
    
    asset['type'] = asset_type
    asset['schema_version'] = '1.6.0'
    
    # Capsule 需要 gene 引用（先使用占位符）
    if asset_type == 'Capsule' and gene_id:
        asset['gene'] = gene_id
    
    # 移除 asset_id
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    
    if asset_type == 'Gene':
        # 计算 Gene asset_id
        gene_canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        gene_id = f"sha256:{hashlib.sha256(gene_canonical.encode('utf-8')).hexdigest()}"
        asset['gene'] = gene_id  # 添加到资产中（虽然 publish 时不需要）
    
    assets_without_id.append(asset_copy)
    print(f"{asset_type}: 准备验证...")

# 创建 validate 信封
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
        "assets": assets_without_id
    }
}

print(f"\n🔍 调用 validate...")
result = client._send_request('/a2a/validate', envelope)

print(f"\n验证结果：{result.get('error', 'Success')}")

# 检查 computed_assets
payload = result.get('payload', {})
computed_assets = payload.get('computed_assets', [])

if computed_assets:
    print(f"\n✅ Hub 计算的 asset_id:")
    for i, asset in enumerate(computed_assets):
        computed_id = asset.get('computed_asset_id', 'N/A')
        print(f"  [{i}] {computed_id[:60]}...")
else:
    print(f"\n❌ 未找到 computed_assets")
    print(f"完整响应:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
