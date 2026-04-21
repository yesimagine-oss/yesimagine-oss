#!/usr/bin/env python3
"""
测试发布单个资产包 - 打印完整错误详情
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

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
result = client.hello()
print(f"✅ 认证成功：hub_node_id={result.get('data', {}).get('hub_node_id')}")

# 测试第一个资产包
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

with open(asset_dir / 'gene.json', 'r', encoding='utf-8') as f:
    gene = json.load(f)

gene['type'] = 'Gene'
gene['schema_version'] = '1.6.0'

# 计算 gene_id
gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
gene_canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
gene_id = f"sha256:{hashlib.sha256(gene_canonical.encode('utf-8')).hexdigest()}"
gene['asset_id'] = gene_id

print(f"\n📦 Gene 内容:")
print(json.dumps(gene, indent=2, ensure_ascii=False))

# 创建发布信封
timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
message_id = f"msg_{int(time.time() * 1000)}"

envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": message_id,
    "sender_id": NODE_ID,
    "timestamp": timestamp,
    "payload": {"assets": [gene]}
}

print(f"\n📦 发布信封:")
print(json.dumps(envelope, indent=2, ensure_ascii=False)[:1000])

# 发布 Gene
print(f"\n发布 Gene...")
result = client._send_request('/a2a/publish', envelope)

print(f"\n📊 Hub 返回结果:")
print(json.dumps(result, indent=2, ensure_ascii=False))
