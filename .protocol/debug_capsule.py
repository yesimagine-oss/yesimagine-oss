#!/usr/bin/env python3
"""
🔍 調試 Capsule asset_id 計算
"""

import json
import hashlib

def compute_asset_id(asset_dict):
    asset_copy = {k: v for k, v in asset_dict.items() if k != 'asset_id'}
    canonical_json = json.dumps(asset_copy, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    hash_obj = hashlib.sha256(canonical_json.encode('utf-8'))
    return f"sha256:{hash_obj.hexdigest()}", canonical_json

# 創建 Capsule
gene_asset_id = "sha256:48ed34fa36949dc429b56335497efd6b1617fc56885d10f1b427d6c8d6e65bfa"

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

# 計算 asset_id
capsule_asset_id, canonical_json = compute_asset_id(capsule)

print(f"Capsule asset_id: {capsule_asset_id}")
print(f"\nCanonical JSON:")
print(canonical_json)
print(f"\nJSON 長度：{len(canonical_json)}")
