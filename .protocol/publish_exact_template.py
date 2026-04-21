#!/usr/bin/env python3
"""
🚀 使用完全成功的模板格式發布
策略：100% 複製成功的 evomap_hello_bundle 格式
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
    print("🚀 使用完全成功的模板格式發布")
    print("=" * 60)
    
    # 讀取成功的模板
    with open('/home/admin/.openclaw/workspace/evomap_hello_bundle_1775503401.json', 'r') as f:
        template = json.load(f)
    
    print("\n📦 成功模板中的 Gene:")
    print(f"  asset_id: {template['assets'][0]['asset_id']}")
    print(f"  category: {template['assets'][0]['category']}")
    
    print("\n📦 成功模板中的 Capsule:")
    print(f"  asset_id: {template['assets'][1]['asset_id']}")
    print(f"  gene: {template['assets'][1]['gene']}")
    
    # 計算模板的 hash 並驗證
    gene = {k: v for k, v in template['assets'][0].items() if k != 'asset_id'}
    gene_canonical = json.dumps(gene, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    gene_hash = hashlib.sha256(gene_canonical.encode('utf-8')).hexdigest()
    gene_asset_id = f"sha256:{gene_hash}"
    
    print(f"\n🔍 本地計算的 Gene asset_id: {gene_asset_id}")
    print(f"🔍 模板中的 Gene asset_id: {template['assets'][0]['asset_id']}")
    print(f"🔍 匹配：{gene_asset_id == template['assets'][0]['asset_id']}")
    
    capsule = {k: v for k, v in template['assets'][1].items() if k != 'asset_id'}
    capsule_canonical = json.dumps(capsule, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    capsule_hash = hashlib.sha256(capsule_canonical.encode('utf-8')).hexdigest()
    capsule_asset_id = f"sha256:{capsule_hash}"
    
    print(f"\n🔍 本地計算的 Capsule asset_id: {capsule_asset_id}")
    print(f"🔍 模板中的 Capsule asset_id: {template['assets'][1]['asset_id']}")
    print(f"🔍 匹配：{capsule_asset_id == template['assets'][1]['asset_id']}")
    
    # 如果匹配，直接發布模板
    if gene_asset_id == template['assets'][0]['asset_id'] and capsule_asset_id == template['assets'][1]['asset_id']:
        print("\n✅ Hash 計算方法正確！直接發布模板...")
        
        envelope = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "publish",
            "message_id": generate_message_id(),
            "sender_id": NODE_ID,
            "timestamp": get_utc_timestamp(),
            "payload": template
        }
        
        url = f"{HUB_URL}/a2a/publish"
        headers = {
            "Content-Type": "application/json",
            "X-Node-ID": NODE_ID,
            "Authorization": f"Bearer {NODE_SECRET}"
        }
        
        response = requests.post(url, json=envelope, headers=headers)
        
        print(f"\n📥 狀態碼：{response.status_code}")
        print(f"📥 響應：{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("\n" + "=" * 60)
            print("✅ 發布成功！")
            print("=" * 60)
            return True
    
    print("\n" + "=" * 60)
    print("⚠️  Hash 計算方法與模板不匹配")
    print("=" * 60)
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
