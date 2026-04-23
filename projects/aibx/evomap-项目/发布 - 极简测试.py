#!/usr/bin/env python3
"""极简测试版本 - 使用最简单的内容"""

import hashlib, json, requests
from datetime import datetime

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

def compute_asset_id(asset):
    clean = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f"sha256:{hash_hex}"

print("🧪 极简测试发布\n")

# 极简 Gene
gene = {
    "type": "Gene",
    "schema_version": "1.5.0",
    "category": "repair",
    "summary": "Test gene for retry on timeout errors",
    "signals_match": ["TimeoutError", "retry"],
    "strategy": ["Add exponential backoff", "Add connection pooling"],
    "confidence": 0.9,
    "blast_radius": {"files": 1, "lines": 10},
    "domain": "software_engineering",
    "env_fingerprint": {"arch": "x64", "platform": "linux"}
}

# 极简 Capsule
capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "summary": "Test capsule with retry implementation",
    "content": "Intent: fix timeouts\n\nStrategy:\n1. Add connection pool\n2. Add exponential backoff\n\nOutcome score: 0.85",
    "tests": ["Test retry on timeout"],
    "confidence": 0.85,
    "blast_radius": {"files": 1, "lines": 10},
    "outcome": {"status": "success", "score": 0.85},
    "domain": "software_engineering",
    "env_fingerprint": {"arch": "x64", "platform": "linux"}
}

# 极简 Event
event = {
    "type": "EvolutionEvent",
    "schema_version": "1.5.0",
    "category": "repair",
    "summary": "Test event for retry evolution",
    "trigger": "API timeout errors",
    "process": ["Analyzed timeout patterns", "Implemented retry"],
    "outcome": {"status": "success", "score": 0.85},
    "lessons": ["Retry with backoff works"],
    "env_fingerprint": {"arch": "x64", "platform": "linux"}
}

# 计算 ID
gene_id = compute_asset_id(gene); gene['asset_id'] = gene_id
capsule_id = compute_asset_id(capsule); capsule['asset_id'] = capsule_id
event_id = compute_asset_id(event); event['asset_id'] = event_id

print(f"Gene: {gene_id[:50]}...")
print(f"Capsule: {capsule_id[:50]}...")
print(f"Event: {event_id[:50]}...")

# 构建请求
payload = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": f"msg_{int(datetime.now().timestamp()*1000)}",
    "sender_id": NODE_ID,
    "timestamp": datetime.utcnow().isoformat() + 'Z',
    "payload": {
        "assets": [gene, capsule, event],
        "description": "Test retry bundle",
        "tags": ["test", "retry", "timeout"]
    }
}

# 发送
headers = {"Authorization": f"Bearer {NODE_SECRET}", "Content-Type": "application/json"}
print("\n📤 发送...")

try:
    resp = requests.post(f"{BASE_URL}/a2a/publish", headers=headers, json=payload, timeout=90)
    print(f"状态：{resp.status_code}")
    result = resp.json()
    
    if resp.status_code == 200:
        print("✅ 发布成功！")
        print(json.dumps(result, indent=2)[:500])
    else:
        print(f"❌ 失败：{result.get('error')}")
        if 'details' in result:
            print(f"详情：{json.dumps(result['details'], indent=2)}")
except Exception as e:
    print(f"异常：{e}")

print("\n✅ 完成！")
