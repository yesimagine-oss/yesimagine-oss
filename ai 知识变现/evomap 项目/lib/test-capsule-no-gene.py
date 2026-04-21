#!/usr/bin/env python3
"""
测试：Capsule 不包含 gene 字段
"""
import json
import hashlib
from pathlib import Path

capsule_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/capsule.json")
with open(capsule_file, 'r', encoding='utf-8') as f:
    capsule = json.load(f)

capsule['type'] = 'Capsule'
capsule['schema_version'] = '1.6.0'

# 测试 1: 包含 gene
capsule_with_gene = {k: v for k, v in capsule.items() if k != 'asset_id'}
id_with_gene = f"sha256:{hashlib.sha256(json.dumps(capsule_with_gene, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"

# 测试 2: 不包含 gene
capsule_no_gene = {k: v for k, v in capsule.items() if k != 'asset_id' and k != 'gene'}
id_no_gene = f"sha256:{hashlib.sha256(json.dumps(capsule_no_gene, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"

print(f"Capsule asset_id:")
print(f"  包含 gene: {id_with_gene}")
print(f"  不含 gene: {id_no_gene}")

# 测试 3: gene 作为对象引用（而不是字符串）
capsule_gene_obj = {k: v for k, v in capsule.items() if k != 'asset_id'}
capsule_gene_obj['gene'] = {"asset_id": capsule.get('gene')}
id_gene_obj = f"sha256:{hashlib.sha256(json.dumps(capsule_gene_obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"

print(f"  gene 作为对象：{id_gene_obj}")
