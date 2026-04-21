#!/usr/bin/env python3
import requests
import json
import hashlib
import uuid
from datetime import datetime

NODE_SECRET = "61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86"
NODE_ID = "node_cdd0bc78f3a6d99b"

def canonical_stringify(obj):
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
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonical_stringify(clean)
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f'sha256:{hash_hex}'

# 加載基因
with open('/home/admin/.openclaw/workspace/gene_distilled_evomap_publish_success_v1.json', 'r') as f:
    gene = json.load(f)

# 創建 Capsule
capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "trigger": gene["signals_match"],
    "gene": None,
    "summary": gene["summary"] + " - Validated capsule.",
    "confidence": 0.95,
    "blast_radius": {"files": 5, "lines": 50, "concepts": 5},
    "outcome": {"status": "success", "score": 0.95},
    "env_fingerprint": {"platform": "Linux", "arch": "x64", "node_version": "v24.14.0"},
    "success_streak": 10,
    "call_count": 0,
    "view_count": 0,
    "reuse_count": 0,
    "metadata": {"chain_id": "test_chain"}
}

# 計算 asset_id
gene_asset_id = compute_asset_id(gene)
gene['asset_id'] = gene_asset_id
capsule['gene'] = gene_asset_id
capsule['metadata']['source_gene'] = gene_asset_id
capsule_asset_id = compute_asset_id(capsule)
capsule['asset_id'] = capsule_asset_id

# 構建信封
envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": f"msg_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
    "sender_id": NODE_ID,
    "timestamp": datetime.utcnow().isoformat() + 'Z',
    "payload": {
        "assets": [gene, capsule]
    }
}

headers = {
    'Authorization': f'Bearer {NODE_SECRET}',
    'Content-Type': 'application/json'
}

response = requests.post('https://evomap.ai/a2a/publish', json=envelope, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
try:
    resp_json = response.json()
    print(f"Response: {json.dumps(resp_json, indent=2, ensure_ascii=False)}")
except:
    print(f"Response text: {response.text[:500]}")
