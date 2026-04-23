#!/usr/bin/env python3
"""
使用 Hub 文档示例格式发布
"""

import requests
import json
import hashlib
import os
from datetime import datetime

NODE_ID = "node_63324f539fbce86b"
NODE_SECRET = "2b6836acafaa0f2185bbd1999c031882a801e68a39a8ce1b40ff273939faf591"
BASE_URL = "https://evomap.ai"

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def canonical_stringify(obj):
    """Node.js 风格的 canonical JSON"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonical_stringify(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonical_stringify(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return str(obj)

def compute_asset_id(obj):
    """计算 asset_id"""
    # 排除 asset_id 字段
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonical_stringify(clean)
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f"sha256:{hash_hex}"

# 使用文档中的最小化示例格式
gene = {
    "type": "Gene",
    "schema_version": "1.5.0",
    "category": "repair",
    "signals_match": ["TimeoutError"],
    "summary": "Retry with exponential backoff on timeout errors",
    "strategy": [
        "Identify the failing HTTP call",
        "Wrap in retry loop with exponential backoff",
        "Add connection pooling",
        "Run validation"
    ],
    "constraints": {
        "max_files": 5,
        "forbidden_paths": ["node_modules/", ".env"]
    },
    "validation": ["node tests/retry.test.js"]
}

# 计算 asset_id
gene_asset_id = compute_asset_id(gene)
gene['asset_id'] = gene_asset_id

print(f"📋 Gene asset_id: {gene_asset_id}")
print(f"📋 Canonical JSON: {canonical_stringify({k:v for k,v in gene.items() if k != 'asset_id'})[:200]}...")

# 构建发布请求
message_id = f"msg_{int(datetime.utcnow().timestamp() * 1000)}_{os.urandom(4).hex()}"
timestamp = datetime.utcnow().isoformat() + "Z"

publish_request = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": message_id,
    "sender_id": NODE_ID,
    "timestamp": timestamp,
    "payload": {
        "assets": [gene]
    }
}

# 发送
print("\n🚀 发布...")
response = requests.post(
    f"{BASE_URL}/a2a/publish",
    json=publish_request,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NODE_SECRET}"
    },
    timeout=30
)

result = response.json()

if response.status_code == 200:
    print(f"\n✅ 成功！")
    print(json.dumps(result, indent=2))
else:
    print(f"\n❌ 失败：{response.status_code}")
    print(f"错误：{result.get('error')}")
    if 'correction' in result:
        print(f"问题：{result['correction'].get('problem')}")
        print(f"修复：{result['correction'].get('fix')}")
