#!/usr/bin/env python3
"""
分步发布：
1. 先发布 Gene
2. 用 Hub 接受的 Gene asset_id 构建 Capsule
3. 发布 Bundle
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

client = GAPA2AClient(NODE_ID, NODE_SECRET, "https://evomap.ai")
result = client.hello()
print(f"✅ 认证成功")

asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

# 步骤 1: 读取并发布 Gene
print(f"\n📦 步骤 1: 发布 Gene...")
with open(asset_dir / 'gene.json', 'r', encoding='utf-8') as f:
    gene = json.load(f)

gene['type'] = 'Gene'
gene['schema_version'] = '1.6.0'

# 计算 gene_id
gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
gene_canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
gene_id = f"sha256:{hashlib.sha256(gene_canonical.encode('utf-8')).hexdigest()}"
gene['asset_id'] = gene_id

print(f"Gene asset_id: {gene_id[:60]}...")

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

result = client._send_request('/a2a/publish', envelope)

if result.get('error'):
    print(f"❌ Gene 发布失败：{result.get('error')}")
    details = result.get('data', {}).get('details', '')
    if details:
        print(f"详情：{details[:500]}")
else:
    print(f"✅ Gene 发布成功！")
    print(f"Hub 返回：{json.dumps(result, indent=2)[:500]}")
