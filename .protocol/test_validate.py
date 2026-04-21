#!/usr/bin/env python3
import requests
import json
import uuid
from datetime import datetime

NODE_SECRET = "61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86"

# 加載一個真實的基因
with open('/home/admin/.openclaw/workspace/gene_distilled_evomap_publish_success_v1.json', 'r') as f:
    gene = json.load(f)

# 測試完整的 validate 請求
envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "validate",
    "message_id": f"msg_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
    "sender_id": "node_cdd0bc78f3a6d99b",
    "timestamp": datetime.utcnow().isoformat() + 'Z',
    "payload": {
        "assets": [gene]
    }
}

headers = {
    'Authorization': f'Bearer {NODE_SECRET}',
    'Content-Type': 'application/json'
}

response = requests.post('https://evomap.ai/a2a/validate', json=envelope, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
try:
    resp_json = response.json()
    print(f"Response: {json.dumps(resp_json, indent=2, ensure_ascii=False)[:1000]}")
except:
    print(f"Response: {response.text[:1000]}")
