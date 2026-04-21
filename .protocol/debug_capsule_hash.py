#!/usr/bin/env python3
"""
🔍 調試 Capsule asset_id 計算
"""

import json
import hashlib

def compute_asset_id(asset_dict, debug=False):
    asset_copy = {k: v for k, v in asset_dict.items() if k != 'asset_id'}
    canonical_json = json.dumps(asset_copy, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    hash_obj = hashlib.sha256(canonical_json.encode('utf-8'))
    asset_id = f"sha256:{hash_obj.hexdigest()}"
    
    if debug:
        print(f"Canonical JSON ({len(canonical_json)} chars):")
        print(canonical_json)
        print()
    
    return asset_id

# 創建與腳本中完全相同的 Capsule
gene_asset_id = "sha256:ba03282a62b36c0e7043ee8e3336d176b69ba3ad4cccee258ce6ffdb216689c1"

capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "trigger": ["test", "simple"],
    "gene": gene_asset_id,
    "summary": "Test capsule for asset_id verification with Hub",
    "confidence": 0.9,
    "blast_radius": {"files": 1, "lines": 5, "concepts": 2},
    "outcome": {"status": "success", "score": 0.9},
    "env_fingerprint": {"node_version": "v24.14.0", "platform": "linux", "arch": "x64"},
    "success_streak": 1,
    "call_count": 0,
    "view_count": 0,
    "reuse_count": 0,
    "metadata": {"chain_id": "chain_test_20260413", "test": True}
}

capsule_asset_id = compute_asset_id(capsule, debug=True)
print(f"Capsule asset_id: {capsule_asset_id}")

# 嘗試不同的 metadata 格式（test 作為字符串而不是布爾值）
capsule2 = capsule.copy()
capsule2['metadata'] = {"chain_id": "chain_test_20260413", "test": "true"}
capsule2_asset_id = compute_asset_id(capsule2, debug=False)
print(f"Capsule asset_id (test as string): {capsule2_asset_id}")
