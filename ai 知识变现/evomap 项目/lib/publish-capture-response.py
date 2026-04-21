#!/usr/bin/env python3
"""
发布完整 Bundle 并捕获 Hub 返回的 computed_asset_id
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

client = GAPA2AClient(NODE_ID, NODE_SECRET, "https://evomap.ai")
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

print("🚀 发布 Bundle...")
result = client._send_request('/a2a/publish', envelope)

# 完整输出响应
print(f"\n完整响应:")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 尝试提取 computed_asset_id
if result.get('data', {}).get('details'):
    try:
        details = json.loads(result['data']['details'])
        print(f"\n\n解析后的错误详情:")
        print(json.dumps(details, indent=2, ensure_ascii=False))
        
        # 查找所有 sha256 开头的值
        def find_sha256(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, str) and v.startswith('sha256:'):
                        print(f"\n找到 asset_id ({path}.{k}): {v}")
                    find_sha256(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    find_sha256(v, f"{path}[{i}]")
        
        find_sha256(details)
    except Exception as e:
        print(f"\n解析失败：{e}")
