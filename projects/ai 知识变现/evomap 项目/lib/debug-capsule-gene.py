#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path

# 读取 Gene
gene_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/gene.json")
with open(gene_file, 'r', encoding='utf-8') as f:
    gene = json.load(f)

gene['type'] = 'Gene'
gene['schema_version'] = '1.6.0'

# 计算 Gene asset_id
gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
gene_canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
gene_id = f"sha256:{hashlib.sha256(gene_canonical.encode('utf-8')).hexdigest()}"

print(f"Gene asset_id:")
print(f"  {gene_id}")

# 读取 Capsule
capsule_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/capsule.json")
with open(capsule_file, 'r', encoding='utf-8') as f:
    capsule = json.load(f)

capsule['type'] = 'Capsule'
capsule['schema_version'] = '1.6.0'
capsule['gene'] = gene_id

# 计算 Capsule asset_id
capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
capsule_canonical = json.dumps(capsule_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
capsule_id = f"sha256:{hashlib.sha256(capsule_canonical.encode('utf-8')).hexdigest()}"

print(f"\nCapsule asset_id (包含 gene 引用):")
print(f"  {capsule_id}")

print(f"\nCapsule Canonical JSON:")
print(capsule_canonical[:800])
