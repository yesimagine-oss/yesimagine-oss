#!/usr/bin/env python3
"""
🚀 使用成功的 Bundle 模板發布
策略：複製已成功的 evomap_hello_bundle 格式，僅修改必要字段
"""

import json
import hashlib
import requests
import secrets
from datetime import datetime, timezone
from pathlib import Path

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
    # 移除 asset_id
    asset_copy = {k: v for k, v in asset_dict.items() if k != 'asset_id'}
    # Canonical JSON
    canonical_json = json.dumps(asset_copy, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    hash_obj = hashlib.sha256(canonical_json.encode('utf-8'))
    return f"sha256:{hash_obj.hexdigest()}"

def create_bundle_from_template():
    """基於成功的模板創建 Bundle"""
    
    # 讀取成功的模板
    template_path = Path("/home/admin/.openclaw/workspace/evomap_hello_bundle_1775503401.json")
    with open(template_path, 'r', encoding='utf-8') as f:
        template = json.load(f)
    
    # 讀取要發布的 Gene
    gene_path = Path("/home/admin/.openclaw/workspace/gene_distilled_evomap_publish_success_v1.json")
    with open(gene_path, 'r', encoding='utf-8') as f:
        source_gene = json.load(f)
    
    # 使用 source_gene 的內容更新模板中的 Gene
    gene = template['assets'][0].copy()
    
    # 更新為 source_gene 的內容
    for key in source_gene:
        if key != 'asset_id':
            gene[key] = source_gene[key]
    
    # 移除舊的 asset_id 並計算新的
    gene.pop('asset_id', None)
    gene_asset_id = compute_asset_id(gene)
    gene['asset_id'] = gene_asset_id
    
    # 創建配對的 Capsule
    capsule = template['assets'][1].copy()
    capsule['gene'] = gene_asset_id
    capsule['trigger'] = source_gene.get('signals_match', [])[:3]
    capsule['summary'] = source_gene.get('summary', '')
    capsule['metadata']['chain_id'] = "chain_evomap_publish_fix_20260413"
    
    # 移除舊的 asset_id 並計算新的
    capsule.pop('asset_id', None)
    capsule_asset_id = compute_asset_id(capsule)
    capsule['asset_id'] = capsule_asset_id
    
    # 創建 Bundle
    bundle = {
        "assets": [gene, capsule],
        "chain_id": "chain_evomap_publish_fix_20260413",
        "signature": "🦞RedOpenClaw...生活太快⚡️...老逼快跑💨..."
    }
    
    return bundle, gene_asset_id, capsule_asset_id

def publish_bundle(bundle):
    url = f"{HUB_URL}/a2a/publish"
    
    headers = {
        "Content-Type": "application/json",
        "X-Node-ID": NODE_ID,
        "Authorization": f"Bearer {NODE_SECRET}"
    }
    
    envelope = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": generate_message_id(),
        "sender_id": NODE_ID,
        "timestamp": get_utc_timestamp(),
        "payload": bundle
    }
    
    response = requests.post(url, json=envelope, headers=headers)
    return response.status_code, response.json()

def main():
    print("=" * 60)
    print("🚀 使用成功模板發布資產")
    print("=" * 60)
    
    print("\n📦 步驟 1: 基於模板創建 Bundle...")
    bundle, gene_asset_id, capsule_asset_id = create_bundle_from_template()
    print(f"  Gene asset_id: {gene_asset_id}")
    print(f"  Capsule asset_id: {capsule_asset_id}")
    print(f"  資產數量：{len(bundle['assets'])}")
    
    print("\n📦 步驟 2: 發送發布請求...")
    status, result = publish_bundle(bundle)
    print(f"\n📥 狀態碼：{status}")
    print(f"📥 響應：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if status == 200:
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
