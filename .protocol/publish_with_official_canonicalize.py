#!/usr/bin/env python3
"""
🚀 使用官方 canonicalize 算法發布資產
關鍵：官方算法與 Python json.dumps 不同！
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

def canonicalize(obj):
    """
    官方 canonicalize 實現 (複製自 contentHash.js)
    """
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        if not isinstance(obj, (int, float)) or (isinstance(obj, float) and (obj != obj or obj == float('inf') or obj == float('-inf'))):
            return 'null'
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = []
        for k in keys:
            pairs.append(json.dumps(k, ensure_ascii=False) + ':' + canonicalize(obj[k]))
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj):
    """計算 asset_id - 排除 asset_id 字段"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return f"sha256:{hash_hex}"

def generate_message_id():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    random_hex = secrets.token_hex(4)
    return f"msg_{timestamp}_{random_hex}"

def get_utc_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def main():
    print("=" * 60)
    print("🚀 使用官方 canonicalize 算法發布")
    print("=" * 60)
    
    # 讀取成功的模板
    with open('/home/admin/.openclaw/workspace/evomap_hello_bundle_1775503401.json', 'r') as f:
        template = json.load(f)
    
    # 保存原始的 asset_id
    original_gene_asset_id = template['assets'][0]['asset_id']
    original_capsule_asset_id = template['assets'][1]['asset_id']
    
    # 測試 Gene 的 hash
    gene = template['assets'][0].copy()
    gene.pop('asset_id', None)
    gene_asset_id = compute_asset_id(gene)
    
    print(f"\n🔍 使用官方算法計算的 Gene asset_id:")
    print(f"   {gene_asset_id}")
    print(f"🔍 模板中的 Gene asset_id:")
    print(f"   {original_gene_asset_id}")
    print(f"🔍 匹配：{gene_asset_id == original_gene_asset_id}")
    
    # 測試 Capsule 的 hash
    capsule = template['assets'][1].copy()
    capsule.pop('asset_id', None)
    capsule_asset_id = compute_asset_id(capsule)
    
    print(f"\n🔍 使用官方算法計算的 Capsule asset_id:")
    print(f"   {capsule_asset_id}")
    print(f"🔍 模板中的 Capsule asset_id:")
    print(f"   {original_capsule_asset_id}")
    print(f"🔍 匹配：{capsule_asset_id == original_capsule_asset_id}")
    
    # 如果匹配，直接發布模板
    if gene_asset_id == original_gene_asset_id and capsule_asset_id == original_capsule_asset_id:
        print("\n✅ Hash 算法正確！直接發布模板...")
        
        # 重新加載模板（因為上面 pop 了 asset_id）
        with open('/home/admin/.openclaw/workspace/evomap_hello_bundle_1775503401.json', 'r') as f:
            template = json.load(f)
        
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
    else:
        print("\n⚠️  Hash 算法仍不匹配，需要進一步調試")
    
    print("\n" + "=" * 60)
    print("⚠️  發布失敗")
    print("=" * 60)
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
