#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path

asset_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/capsule.json")
with open(asset_file, 'r', encoding='utf-8') as f:
    asset = json.load(f)

asset['type'] = 'Capsule'
asset['schema_version'] = '1.5.0'

# 移除 asset_id（如果有）
asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}

# Canonical JSON
canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
print(f"Canonical JSON:")
print(canonical)
print(f"\n长度：{len(canonical)}")

# 计算哈希
hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
asset_id = f"sha256:{hash_hex}"
print(f"\n计算的 asset_id:")
print(asset_id)
