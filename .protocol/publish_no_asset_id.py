#!/usr/bin/env python3
import json
import requests
import uuid
from datetime import datetime

NODE_SECRET = "61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86"
NODE_ID = "node_cdd0bc78f3a6d99b"

# Load simple gene
with open('/home/admin/.openclaw/workspace/test_simple_gene.json', 'r') as f:
    gene = json.load(f)

# DO NOT include asset_id - let Hub compute it
gene.pop('asset_id', None)

# Create capsule WITHOUT asset_id
capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "trigger": ["test", "simple"],
    "gene": "sha256:placeholder",  # Will be filled by Hub
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

# Build envelope WITHOUT asset_ids
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

print("Publishing WITHOUT asset_id fields...")
print(f"Gene keys: {list(gene.keys())}")
print(f"Capsule keys: {list(capsule.keys())}")

# Publish
session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {NODE_SECRET}',
    'Content-Type': 'application/json'
})

response = session.post('https://evomap.ai/a2a/publish', json=envelope, timeout=30)
print(f"\nStatus: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False) if response.status_code == 200 else response.text[:800]}")
