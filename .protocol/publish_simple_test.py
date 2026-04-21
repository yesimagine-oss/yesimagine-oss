#!/usr/bin/env python3
import json
import hashlib
import requests
import uuid
from datetime import datetime

NODE_SECRET = "61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86"
NODE_ID = "node_cdd0bc78f3a6d99b"

# Load simple gene
with open('/home/admin/.openclaw/workspace/test_simple_gene.json', 'r') as f:
    gene = json.load(f)

# Remove asset_id if exists
gene.pop('asset_id', None)

# Compute asset_id using json.dumps with sort_keys
canonical = json.dumps(gene, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
gene_asset_id = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
gene['asset_id'] = gene_asset_id

# Create simple capsule
capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "trigger": ["test", "simple"],
    "gene": gene_asset_id,
    "summary": "Test capsule for simple gene",
    "confidence": 0.9,
    "blast_radius": {"files": 1, "lines": 10, "concepts": 2},
    "outcome": {"status": "success", "score": 0.9},
    "env_fingerprint": {"platform": "Linux", "arch": "x64", "node_version": "v24.14.0"},
    "success_streak": 1,
    "call_count": 0,
    "view_count": 0,
    "reuse_count": 0,
    "metadata": {"chain_id": "test_chain"}
}

# Compute capsule asset_id (remove asset_id first, then compute)
capsule_for_hash = {k: v for k, v in capsule.items() if k != 'asset_id'}
capsule_canonical = json.dumps(capsule_for_hash, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
capsule_asset_id = f'sha256:{hashlib.sha256(capsule_canonical.encode()).hexdigest()}'
capsule['asset_id'] = capsule_asset_id

print(f"Gene asset_id: {gene_asset_id}")
print(f"Capsule asset_id: {capsule_asset_id}")
print(f"\nGene canonical (first 150 chars): {canonical[:150]}")

# Build envelope
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

# Publish
session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {NODE_SECRET}',
    'Content-Type': 'application/json'
})

response = session.post('https://evomap.ai/a2a/publish', json=envelope, timeout=30)
print(f"\nStatus: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False) if response.status_code == 200 else response.text[:500]}")
