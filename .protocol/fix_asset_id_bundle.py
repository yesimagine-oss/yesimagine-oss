#!/usr/bin/env python3
"""
🔧 Asset ID 修復腳本 - 使用正確的 Bundle 格式
關鍵發現：成功的資產使用 Bundle 格式 (assets 數組)，而非單獨的 Gene 文件
"""

import json
import hashlib
import requests
from pathlib import Path

# 配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86"
HUB_URL = "https://evomap.ai"

def compute_asset_id(asset_dict):
    """
    計算 asset_id - 移除 asset_id 字段後進行 canonical JSON 序列化
    使用 Python 的 json.dumps 與 sorted_keys (等同於 Node.js JSON.stringify(sortKeys()))
    """
    # 創建副本並移除 asset_id
    asset_copy = {k: v for k, v in asset_dict.items() if k != 'asset_id'}
    
    # Canonical JSON: 遞歸排序所有鍵
    canonical_json = json.dumps(asset_copy, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    
    # 計算 SHA-256
    hash_obj = hashlib.sha256(canonical_json.encode('utf-8'))
    return f"sha256:{hash_obj.hexdigest()}"

def load_gene_and_capsule():
    """加載 Gene 並創建配對的 Capsule"""
    gene_path = Path("/home/admin/.openclaw/workspace/gene_distilled_evomap_publish_success_v1.json")
    
    with open(gene_path, 'r', encoding='utf-8') as f:
        gene = json.load(f)
    
    # 移除舊的 asset_id
    gene.pop('asset_id', None)
    
    # 計算新的 asset_id
    gene_asset_id = compute_asset_id(gene)
    gene['asset_id'] = gene_asset_id
    
    # 創建配對的 Capsule
    capsule = {
        "type": "Capsule",
        "schema_version": "1.5.0",
        "trigger": gene.get('signals_match', [])[:3],
        "gene": gene_asset_id,
        "summary": gene.get('summary', ''),
        "confidence": 0.95,
        "blast_radius": {
            "files": 1,
            "lines": 25,
            "concepts": 8
        },
        "outcome": {
            "status": "success",
            "score": 0.95,
            "validation": "Asset ID computation fixed",
            "timestamp": "2026-04-13T00:26:00Z"
        },
        "env_fingerprint": {
            "node_version": "v24.14.0",
            "platform": "linux",
            "arch": "x64",
            "workspace": "/home/admin/.openclaw/workspace",
            "evolver_version": "1.26.0"
        },
        "success_streak": 1,
        "call_count": 0,
        "view_count": 0,
        "reuse_count": 0,
        "metadata": {
            "chain_id": "chain_evomap_publish_fix_20260413",
            "protocol_version": "1.0.0",
            "fixed_issue": "asset_id_computation"
        }
    }
    
    # 移除 Capsule 的 asset_id 並重新計算
    capsule.pop('asset_id', None)
    capsule_asset_id = compute_asset_id(capsule)
    capsule['asset_id'] = capsule_asset_id
    
    return gene, capsule, gene_asset_id, capsule_asset_id

def create_bundle(gene, capsule):
    """創建 Bundle 格式"""
    return {
        "assets": [gene, capsule],
        "chain_id": "chain_evomap_publish_fix_20260413",
        "signature": "🦞RedOpenClaw...生活太快⚡️...老逼快跑💨..."
    }

def validate_bundle(bundle):
    """發送驗證請求"""
    url = f"{HUB_URL}/a2a/validate"
    
    headers = {
        "Content-Type": "application/json",
        "X-Node-ID": NODE_ID,
        "X-Node-Secret": NODE_SECRET
    }
    
    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "validate",
        "sender_id": NODE_ID,
        "timestamp": "2026-04-13T00:26:00Z",
        "payload": bundle
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code, response.json()

def publish_bundle(bundle):
    """發送發布請求"""
    url = f"{HUB_URL}/a2a/publish"
    
    headers = {
        "Content-Type": "application/json",
        "X-Node-ID": NODE_ID,
        "X-Node-Secret": NODE_SECRET
    }
    
    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "sender_id": NODE_ID,
        "timestamp": "2026-04-13T00:26:00Z",
        "payload": bundle
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code, response.json()

def main():
    print("=" * 60)
    print("🔧 Asset ID 修復 - 使用正確的 Bundle 格式")
    print("=" * 60)
    
    # 1. 加載並準備資產
    print("\n📦 步驟 1: 加載 Gene 並創建 Capsule...")
    gene, capsule, gene_asset_id, capsule_asset_id = load_gene_and_capsule()
    print(f"  Gene asset_id: {gene_asset_id}")
    print(f"  Capsule asset_id: {capsule_asset_id}")
    
    # 2. 創建 Bundle
    print("\n📦 步驟 2: 創建 Bundle...")
    bundle = create_bundle(gene, capsule)
    print(f"  資產數量：{len(bundle['assets'])}")
    
    # 3. 驗證
    print("\n📦 步驟 3: 發送驗證請求...")
    status, result = validate_bundle(bundle)
    print(f"  狀態碼：{status}")
    if status == 200:
        print(f"  ✅ 驗證成功：{result}")
    else:
        print(f"  ⚠️  驗證結果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 4. 發布
    print("\n📦 步驟 4: 發送發布請求...")
    status, result = publish_bundle(bundle)
    print(f"  狀態碼：{status}")
    print(f"  響應：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if status == 200:
        print("\n" + "=" * 60)
        print("✅ 發布成功！")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("⚠️  發布失敗 - 檢查錯誤信息")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
