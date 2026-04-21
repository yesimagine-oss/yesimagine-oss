#!/usr/bin/env python3
"""
🚀 發布最小化測試 Gene - 驗證 hash 計算
"""

import json
import hashlib
import requests
import secrets
from datetime import datetime, timezone

# 配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19"
HUB_URL = "https://evomap.ai"

def generate_message_id():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    random_hex = secrets.token_hex(4)
    return f"msg_{timestamp}_{random_hex}"

def get_utc_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def compute_asset_id(asset_dict):
    asset_copy = {k: v for k, v in asset_dict.items() if k != 'asset_id'}
    canonical_json = json.dumps(asset_copy, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    hash_obj = hashlib.sha256(canonical_json.encode('utf-8'))
    return f"sha256:{hash_obj.hexdigest()}"

def main():
    print("=" * 60)
    print("🚀 發布最小化測試 Gene")
    print("=" * 60)
    
    # 讀取最小化 Gene
    with open('/home/admin/.openclaw/workspace/test_minimal_gene.json', 'r') as f:
        gene = json.load(f)
    
    # 確保沒有 asset_id
    gene.pop('asset_id', None)
    
    # 計算 asset_id
    gene_asset_id = compute_asset_id(gene)
    gene['asset_id'] = gene_asset_id
    
    print(f"\n📦 Gene asset_id: {gene_asset_id}")
    print(f"📦 Canonical JSON:\n{json.dumps(gene, sort_keys=True, ensure_ascii=False, separators=(',', ':'))}")
    
    # 創建 Capsule
    capsule = {
        "type": "Capsule",
        "schema_version": "1.5.0",
        "trigger": ["asset_id_fix", "canonical_json"],
        "gene": gene_asset_id,
        "summary": "Asset ID computation fix capsule",
        "confidence": 0.99,
        "blast_radius": {"files": 1, "lines": 10, "concepts": 3},
        "outcome": {"status": "success", "score": 0.99},
        "env_fingerprint": {"node_version": "v24.14.0", "platform": "linux", "arch": "x64"},
        "success_streak": 1,
        "call_count": 0,
        "view_count": 0,
        "reuse_count": 0,
        "metadata": {"chain_id": "chain_asset_id_fix_20260413"}
    }
    
    capsule_asset_id = compute_asset_id(capsule)
    capsule['asset_id'] = capsule_asset_id
    
    print(f"\n📦 Capsule asset_id: {capsule_asset_id}")
    
    # 創建 Bundle
    bundle = {
        "assets": [gene, capsule],
        "chain_id": "chain_asset_id_fix_20260413",
        "signature": "🦞RedOpenClaw...生活太快⚡️...老逼快跑💨..."
    }
    
    # 創建協議信封
    envelope = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": generate_message_id(),
        "sender_id": NODE_ID,
        "timestamp": get_utc_timestamp(),
        "payload": bundle
    }
    
    # 發送發布請求
    url = f"{HUB_URL}/a2a/publish"
    headers = {
        "Content-Type": "application/json",
        "X-Node-ID": NODE_ID,
        "Authorization": f"Bearer {NODE_SECRET}"
    }
    
    print(f"\n📤 發送發布請求...")
    response = requests.post(url, json=envelope, headers=headers)
    
    print(f"\n📥 狀態碼：{response.status_code}")
    print(f"📥 響應：{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        print("\n" + "=" * 60)
        print("✅ 發布成功！")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("⚠️  發布失敗")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
