#!/usr/bin/env python3
import json
import hashlib
import sys
sys.path.insert(0, 'lib')
from gep_a2a_client import GAPA2AClient

def canonicalize(obj):
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
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

def compute_asset_id(asset):
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = canonicalize(asset_copy)
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f'sha256:{hash_hex}'

# 测试 Gene
gene = {
    "id": "test_gene_001",
    "type": "Gene",
    "summary": "Test Gene",
    "category": "optimize",
    "schema_version": "1.5.0"
}

gene_asset_id = compute_asset_id(gene)
print(f"Gene Asset ID: {gene_asset_id}")

# 测试 Capsule (包含 gene 的 asset_id)
capsule = {
    "id": "test_capsule_001",
    "type": "Capsule",
    "asset_id": gene_asset_id,  # 引用 Gene
    "summary": "Test Capsule",
    "content": "Test content",
    "schema_version": "1.5.0"
}

capsule_asset_id = compute_asset_id(capsule)
print(f"Capsule Asset ID: {capsule_asset_id}")

# 验证：移除 asset_id 后重新计算
capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
capsule_asset_id_2 = compute_asset_id(capsule_copy)
print(f"Capsule Asset ID (without asset_id field): {capsule_asset_id_2}")

print(f"\n匹配：{capsule_asset_id == capsule_asset_id_2}")
